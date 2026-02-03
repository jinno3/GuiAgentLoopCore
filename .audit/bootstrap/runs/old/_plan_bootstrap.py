#!/usr/bin/env python3
"""Bootstrap v1.1 - Plan and snapshot generation"""
import json
import yaml
from pathlib import Path
from datetime import datetime
import hashlib

WORKDIR = Path("/home/jinno/jinno3/GuiAgentLoopCore")
RUN_DIR = WORKDIR / ".audit/bootstrap/runs/current"

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_directories():
    """Create required directories"""
    (RUN_DIR / "input_snapshot").mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "before").mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "changes").mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "after").mkdir(parents=True, exist_ok=True)
    (RUN_DIR / "verification").mkdir(parents=True, exist_ok=True)

def create_input_snapshots():
    """Phase 2: Create input snapshots"""
    # Load intent
    intent = load_yaml(WORKDIR / ".audit/config/intent.yml")
    
    # Load ontology
    ontology = load_yaml(WORKDIR / ".concept/ontology.yml")
    
    # Create intent digest
    intent_digest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": ".audit/config/intent.yml",
        "mission": intent["mission"],
        "target_users": intent["target_user"],
        "core_value": intent["core_value"],
        "core_functions_count": len(intent["core_functions"]),
        "in_scope_count": len(intent["boundaries"]["in_scope"]),
        "out_of_scope_count": len(intent["boundaries"]["out_of_scope"])
    }
    save_json(intent_digest, RUN_DIR / "input_snapshot/intent_digest.json")
    
    # Create ontology digest
    canonical_terms = ontology.get("canonical_terms", {})
    core_terms = {k: v for k, v in canonical_terms.items() if v.get("layer") == "core"}
    domain_terms = {k: v for k, v in canonical_terms.items() if v.get("layer") == "domain"}
    aux_terms = {k: v for k, v in canonical_terms.items() if v.get("layer") == "aux"}
    
    ontology_digest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": ".concept/ontology.yml",
        "version": ontology.get("version", "unknown"),
        "statistics": {
            "total_terms": len(canonical_terms),
            "by_layer": {
                "core": len(core_terms),
                "domain": len(domain_terms),
                "aux": len(aux_terms)
            }
        },
        "key_terms_for_md": [
            {
                "canonical": term_id,
                "layer": term_data.get("layer"),
                "definition": term_data.get("definition"),
                "synonyms": term_data.get("synonyms", []),
                "should_use_in": ["README.md", "AGENTS.md", "CLAUDE.md"]
            }
            for term_id, term_data in sorted(core_terms.items())[:5]
        ]
    }
    save_json(ontology_digest, RUN_DIR / "input_snapshot/ontology_digest.json")
    
    # Build term normalization map
    term_norm = {}
    for term_id, term_data in canonical_terms.items():
        for syn in term_data.get("synonyms", []):
            term_norm[syn] = term_id
    
    return intent, ontology, term_norm

def capture_before_state():
    """Phase 3: Capture before state"""
    md_files = [
        "README.md", "AGENTS.md", "CLAUDE.md", "GLOSSARY.md",
        "ARCHITECTURE.md", "CONTRIBUTING.md", "SYSTEM_CONSTITUTION.md",
        "PURPOSE.md", "GEMINI.md", "CODEX.md"
    ]
    
    inventory = []
    for md in md_files:
        path = WORKDIR / md
        if path.exists():
            inventory.append({
                "path": md,
                "exists": True,
                "size": path.stat().st_size
            })
        else:
            inventory.append({
                "path": md,
                "exists": False
            })
    
    clarity_score = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "overall_score": 100,  # Will be calculated
        "max_score": 100,
        "files": inventory
    }
    
    save_json({"files": inventory}, RUN_DIR / "before/md_inventory.json")
    save_json(clarity_score, RUN_DIR / "before/clarity_score.json")
    
    return inventory

def create_plan(intent, ontology, term_norm, inventory):
    """Create execution plan"""
    ontology_exists = (WORKDIR / ".concept/ontology.yml").exists()
    
    plan = {
        "run_timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.1",
        "rotation": {
            "deleted_old": True,
            "moved_current_to_old": True
        },
        "input_sources": {
            "audit": {
                "intent_yml": ".audit/config/intent.yml",
                "constraints_yml": ".audit/config/constraints.yml"
            },
            "concept": {
                "ontology_yml": ".concept/ontology.yml",
                "invariants_yml": ".concept/invariants.yml",
                "has_concept": ontology_exists
            }
        },
        "intent_summary": {
            "mission": intent["mission"][:100] + "...",
            "target_user": intent["target_user"][0] if intent["target_user"] else "Unknown",
            "core_value": intent["core_value"][:50] + "..."
        },
        "ontology_summary": {
            "total_terms": len(ontology.get("canonical_terms", {})),
            "core_terms": len([t for t in ontology.get("canonical_terms", {}).values() if t.get("layer") == "core"]),
            "domain_terms": len([t for t in ontology.get("canonical_terms", {}).values() if t.get("layer") == "domain"])
        } if ontology_exists else None,
        "term_normalization": term_norm,
        "existing_mds": [
            {
                "path": item["path"],
                "status": "exists" if item["exists"] else "missing"
            }
            for item in inventory
        ],
        "actions": [
            {"action": "verify", "target": "README.md", "reason": "Check alignment with intent and ontology"},
            {"action": "verify", "target": "AGENTS.md", "reason": "Check alignment with intent and ontology"},
            {"action": "verify", "target": "CLAUDE.md", "reason": "Check alignment with intent and ontology"},
            {"action": "verify", "target": "GLOSSARY.md", "reason": "Check alignment with ontology"},
            {"action": "verify", "target": "SYSTEM_CONSTITUTION.md", "reason": "Check alignment with invariants"},
            {"action": "verify", "target": "PURPOSE.md", "reason": "Check alignment with intent"}
        ]
    }
    
    save_json(plan, RUN_DIR / "plan.json")
    with open(RUN_DIR / "plan.yml", 'w') as f:
        yaml.dump(plan, f, default_flow_style=False, allow_unicode=True)
    
    return plan

def main():
    print("[PLAN] Starting bootstrap plan generation...")
    
    # Phase 2: Create input snapshots
    print("[PLAN] Phase 2: Creating input snapshots...")
    create_directories()
    intent, ontology, term_norm = create_input_snapshots()
    print(f"[PLAN]   - Intent digest created")
    print(f"[PLAN]   - Ontology digest created ({len(ontology.get('canonical_terms', {}))} terms)")
    
    # Phase 3: Capture before state
    print("[PLAN] Phase 3: Capturing before state...")
    inventory = capture_before_state()
    print(f"[PLAN]   - MD inventory: {sum(1 for i in inventory if i['exists'])} existing files")
    
    # Create plan
    print("[PLAN] Creating execution plan...")
    plan = create_plan(intent, ontology, term_norm, inventory)
    print(f"[PLAN]   - Plan created with {len(plan['actions'])} verification actions")
    
    print("[PLAN] Plan generation complete!")

if __name__ == "__main__":
    main()
