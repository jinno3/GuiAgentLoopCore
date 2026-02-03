#!/usr/bin/env python3
"""
MD Bootstrapper v1.1 - Main execution script
Executes the full MD bootstrap workflow with rotation.
"""

import json
import shutil
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any
import re


def rotate_runs(workdir: Path) -> Dict[str, bool]:
    """Phase 0: Execute rotation (2-generation policy)"""
    bootstrap_dir = workdir / ".audit" / "bootstrap" / "runs"
    old_dir = bootstrap_dir / "old"
    current_dir = bootstrap_dir / "current"

    rotation_result = {
        "deleted_old": False,
        "moved_current_to_old": False,
        "created_new_current": False
    }

    # 1. Delete old if exists
    if old_dir.exists():
        shutil.rmtree(old_dir)
        print("[ROTATE] Deleted old run")
        rotation_result["deleted_old"] = True

    # 2. Move current to old if exists
    if current_dir.exists():
        current_dir.rename(old_dir)
        print("[ROTATE] Moved current to old")
        rotation_result["moved_current_to_old"] = True

    # 3. Create new current
    current_dir.mkdir(parents=True, exist_ok=True)
    print("[ROTATE] Created new current")
    rotation_result["created_new_current"] = True

    # Create subdirectories
    (current_dir / "input_snapshot").mkdir(exist_ok=True)
    (current_dir / "before").mkdir(exist_ok=True)
    (current_dir / "changes").mkdir(exist_ok=True)
    (current_dir / "after").mkdir(exist_ok=True)
    (current_dir / "verification").mkdir(exist_ok=True)

    return rotation_result


def load_audit_and_concept(workdir: Path) -> Dict[str, Any]:
    """Phase 1: Load and validate audit + concept inputs"""
    intent_path = workdir / ".audit" / "config" / "intent.yml"
    ontology_path = workdir / ".concept" / "ontology.yml"
    invariants_path = workdir / ".concept" / "invariants.yml"
    ambiguities_path = workdir / ".concept" / "ambiguities.yml"

    # Validate required inputs
    if not intent_path.exists():
        raise FileNotFoundError(f"Required file not found: {intent_path}")

    with open(intent_path, 'r', encoding='utf-8') as f:
        intent = yaml.safe_load(f)

    ontology = None
    if ontology_path.exists():
        with open(ontology_path, 'r', encoding='utf-8') as f:
            ontology = yaml.safe_load(f)

    invariants = None
    if invariants_path.exists():
        with open(invariants_path, 'r', encoding='utf-8') as f:
            invariants = yaml.safe_load(f)

    ambiguities = None
    if ambiguities_path.exists():
        with open(ambiguities_path, 'r', encoding='utf-8') as f:
            ambiguities = yaml.safe_load(f)

    return {
        "intent": intent,
        "ontology": ontology,
        "invariants": invariants,
        "ambiguities": ambiguities
    }


def create_term_normalization_map(ontology: Dict) -> Dict[str, str]:
    """Create synonym -> canonical term mapping"""
    if not ontology or "canonical_terms" not in ontology:
        return {}

    term_map = {}
    for term_id, term_data in ontology["canonical_terms"].items():
        for synonym in term_data.get("synonyms", []):
            term_map[synonym] = term_id

    return term_map


def create_input_snapshots(workdir: Path, inputs: Dict, rotation_result: Dict) -> Dict:
    """Phase 2: Create input snapshots"""
    current_dir = workdir / ".audit" / "bootstrap" / "runs" / "current"
    snapshot_dir = current_dir / "input_snapshot"

    timestamp = datetime.now(timezone.utc).isoformat()

    # Intent digest
    intent = inputs["intent"]
    intent_digest = {
        "timestamp": timestamp,
        "source": ".audit/config/intent.yml",
        "version": intent.get("version", "unknown"),
        "mission_summary": intent.get("mission", "")[:200] + "..." if len(intent.get("mission", "")) > 200 else intent.get("mission", ""),
        "target_users": intent.get("target_user", []),
        "core_value": intent.get("core_value", ""),
        "core_functions_count": len(intent.get("core_functions", [])),
        "boundaries": {
            "in_scope_count": len(intent.get("boundaries", {}).get("in_scope", [])),
            "out_of_scope_count": len(intent.get("boundaries", {}).get("out_of_scope", []))
        }
    }

    with open(snapshot_dir / "intent_digest.json", 'w', encoding='utf-8') as f:
        json.dump(intent_digest, f, indent=2, ensure_ascii=False)

    # Ontology digest (if exists)
    ontology_digest = {
        "timestamp": timestamp,
        "source": ".concept/ontology.yml",
        "exists": inputs["ontology"] is not None
    }

    if inputs["ontology"]:
        ontology = inputs["ontology"]
        canonical_terms = ontology.get("canonical_terms", {})

        # Count by layer
        by_layer = {"core": 0, "domain": 0, "aux": 0}
        by_status = {"stable": 0, "draft": 0}

        for term_id, term_data in canonical_terms.items():
            layer = term_data.get("layer", "unknown")
            status = term_data.get("status", "unknown")
            if layer in by_layer:
                by_layer[layer] += 1
            if status in by_status:
                by_status[status] += 1

        ontology_digest.update({
            "version": ontology.get("version", "unknown"),
            "statistics": {
                "total_terms": len(canonical_terms),
                "by_layer": by_layer,
                "by_status": by_status
            },
            "key_terms_for_md": [
                {
                    "canonical": term_id,
                    "layer": term_data.get("layer"),
                    "definition": term_data.get("definition"),
                    "synonyms": term_data.get("synonyms", []),
                    "status": term_data.get("status")
                }
                for term_id, term_data in list(canonical_terms.items())[:11]  # All 11 terms
            ]
        })

    with open(snapshot_dir / "ontology_digest.json", 'w', encoding='utf-8') as f:
        json.dump(ontology_digest, f, indent=2, ensure_ascii=False)

    return {
        "intent_digest": "intent_digest.json",
        "ontology_digest": "ontology_digest.json",
        "timestamp": timestamp
    }


def scan_existing_mds(workdir: Path) -> List[Dict]:
    """Scan existing MD files"""
    md_files = [
        "README.md", "AGENTS.md", "CLAUDE.md", "SYSTEM_CONSTITUTION.md",
        "PURPOSE.md", "CONTRIBUTING.md", "GLOSSARY.md",
        "GEMINI.md", "CODEX.md", "ARCHITECTURE.md"
    ]

    found = []
    for md_file in md_files:
        path = workdir / md_file
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            found.append({
                "path": md_file,
                "exists": True,
                "size_bytes": len(content.encode('utf-8')),
                "line_count": len(content.splitlines())
            })
        else:
            found.append({
                "path": md_file,
                "exists": False
            })

    return found


def calculate_clarity_score(content: str, intent: Dict, term_map: Dict) -> Dict:
    """Calculate clarity and concept alignment scores"""
    if not content:
        return {"clarity_score": 0, "concept_alignment": {"score": 0, "issues": []}, "issues": []}

    score = 50  # Base score
    issues = []
    alignment_issues = []

    # Check for mission presence
    mission = intent.get("mission", "")
    if mission and mission.lower() in content.lower():
        score += 10
    else:
        issues.append("存在意義（mission）が明示されていない")

    # Check for target users
    target_users = intent.get("target_user", [])
    if any(str(user).lower() in content.lower() for user in target_users):
        score += 10
    else:
        issues.append("対象ユーザーが明示されていない")

    # Check for core value
    core_value = intent.get("core_value", "")
    if core_value and core_value.lower() in content.lower():
        score += 10
    else:
        issues.append("提供価値が明示されていない")

    # Check term normalization (concept alignment)
    alignment_score = 100
    for synonym, canonical in term_map.items():
        # Check if synonym is used (should use canonical instead)
        if re.search(r'\b' + re.escape(synonym) + r'\b', content, re.IGNORECASE):
            alignment_issues.append({
                "found": synonym,
                "should_be": canonical,
                "type": "synonym_usage"
            })
            alignment_score -= 10

    # Check if canonical terms are used
    canonical_count = sum(1 for term in term_map.values()
                         if re.search(r'\b' + re.escape(term) + r'\b', content, re.IGNORECASE))

    if alignment_score < 100:
        issues.append(f"用語が正規形でない（{len(alignment_issues)}箇所）")

    return {
        "clarity_score": min(score, 100),
        "concept_alignment": {
            "score": max(alignment_score, 0),
            "issues": alignment_issues[:10]  # Limit to first 10
        },
        "issues": issues
    }


def capture_before_snapshot(workdir: Path, inputs: Dict, existing_mds: List[Dict]) -> Dict:
    """Phase 3: Capture before snapshot"""
    current_dir = workdir / ".audit" / "bootstrap" / "runs" / "current"
    before_dir = current_dir / "before"

    timestamp = datetime.now(timezone.utc).isoformat()
    term_map = create_term_normalization_map(inputs["ontology"])

    md_inventory = {
        "timestamp": timestamp,
        "files": existing_mds
    }

    with open(before_dir / "md_inventory.json", 'w', encoding='utf-8') as f:
        json.dump(md_inventory, f, indent=2, ensure_ascii=False)

    # Calculate clarity scores
    clarity_scores = {
        "timestamp": timestamp,
        "overall_score": 0,
        "concept_alignment_score": 0,
        "max_score": 100,
        "files": []
    }

    total_clarity = 0
    total_alignment = 0
    file_count = 0

    for md_info in existing_mds:
        if md_info["exists"]:
            path = workdir / md_info["path"]
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            scores = calculate_clarity_score(content, inputs["intent"], term_map)

            file_result = {
                "path": md_info["path"],
                "exists": True,
                "clarity_score": scores["clarity_score"],
                "concept_alignment": scores["concept_alignment"],
                "issues": scores["issues"]
            }
            clarity_scores["files"].append(file_result)

            total_clarity += scores["clarity_score"]
            total_alignment += scores["concept_alignment"]["score"]
            file_count += 1
        else:
            clarity_scores["files"].append({
                "path": md_info["path"],
                "exists": False,
                "clarity_score": 0,
                "concept_alignment": {"score": 0, "issues": []},
                "issues": ["ファイルが存在しない"]
            })

    if file_count > 0:
        clarity_scores["overall_score"] = int(total_clarity / file_count)
        clarity_scores["concept_alignment_score"] = int(total_alignment / file_count)

    with open(before_dir / "clarity_score.json", 'w', encoding='utf-8') as f:
        json.dump(clarity_scores, f, indent=2, ensure_ascii=False)

    return {
        "md_inventory": "md_inventory.json",
        "clarity_score": "clarity_score.json",
        "overall_clarity": clarity_scores["overall_score"],
        "overall_alignment": clarity_scores["concept_alignment_score"]
    }


def create_plan(workdir: Path, inputs: Dict, existing_mds: List[Dict],
                rotation_result: Dict, snapshot_info: Dict, before_scores: Dict) -> Dict:
    """Create execution plan"""
    timestamp = datetime.now(timezone.utc).isoformat()

    intent = inputs["intent"]
    ontology = inputs["ontology"]

    # Determine actions
    actions = []

    # Check which MDs need updates
    for md_info in existing_mds:
        path = md_info["path"]
        if not md_info["exists"]:
            actions.append({
                "action": "create",
                "target": path,
                "reason": f"{path}が存在しない"
            })
        # All existing files should be checked for concept alignment

    plan = {
        "run_timestamp": timestamp,
        "version": "1.1",
        "rotation": rotation_result,
        "input_sources": {
            "audit": {
                "intent_yml": ".audit/config/intent.yml"
            },
            "concept": {
                "ontology_yml": ".concept/ontology.yml",
                "invariants_yml": ".concept/invariants.yml",
                "has_concept": ontology is not None
            }
        },
        "intent_summary": {
            "mission": intent.get("mission", "")[:100] + "...",
            "target_user": intent.get("target_user", [])[:3],
            "core_value": intent.get("core_value", "")[:100] + "..."
        },
        "ontology_summary": {},
        "term_normalization": {},
        "existing_mds": existing_mds,
        "actions": actions,
        "before_scores": before_scores
    }

    if ontology:
        canonical_terms = ontology.get("canonical_terms", {})
        plan["ontology_summary"] = {
            "total_terms": len(canonical_terms),
            "core_terms": sum(1 for t in canonical_terms.values() if t.get("layer") == "core"),
            "domain_terms": sum(1 for t in canonical_terms.values() if t.get("layer") == "domain")
        }

        # Build term normalization map
        term_map = create_term_normalization_map(ontology)
        plan["term_normalization"] = dict(list(term_map.items())[:15])  # First 15

    return plan


def main():
    """Main execution"""
    workdir = Path("/home/jinno/jinno3/GuiAgentLoopCore")

    print("=" * 80)
    print("MD Bootstrapper v1.1 - Starting Execution")
    print("=" * 80)

    # Phase 0: Rotation
    print("\n[Phase 0] Executing rotation...")
    rotation_result = rotate_runs(workdir)

    # Phase 1: Load inputs
    print("\n[Phase 1] Loading audit and concept inputs...")
    inputs = load_audit_and_concept(workdir)
    print(f"  - intent.yml: loaded")
    print(f"  - ontology.yml: {'loaded' if inputs['ontology'] else 'not found'}")
    print(f"  - invariants.yml: {'loaded' if inputs['invariants'] else 'not found'}")
    print(f"  - ambiguities.yml: {'loaded' if inputs['ambiguities'] else 'not found'}")

    # Phase 2: Input snapshots
    print("\n[Phase 2] Creating input snapshots...")
    snapshot_info = create_input_snapshots(workdir, inputs, rotation_result)
    print(f"  - intent_digest.json: created")
    print(f"  - ontology_digest.json: created")

    # Scan existing MDs
    print("\n[Phase 3] Scanning existing MD files...")
    existing_mds = scan_existing_mds(workdir)
    for md in existing_mds:
        status = "✓" if md["exists"] else "✗"
        print(f"  - {status} {md['path']}")

    # Phase 3: Before snapshot
    print("\n[Phase 3] Capturing before snapshot...")
    before_scores = capture_before_snapshot(workdir, inputs, existing_mds)
    print(f"  - Overall clarity score: {before_scores['overall_clarity']}")
    print(f"  - Concept alignment score: {before_scores['overall_alignment']}")

    # Create plan
    print("\n[Phase 1] Creating execution plan...")
    plan = create_plan(workdir, inputs, existing_mds, rotation_result, snapshot_info, before_scores)

    plan_path = workdir / ".audit" / "bootstrap" / "runs" / "current" / "plan.yml"
    with open(plan_path, 'w', encoding='utf-8') as f:
        yaml.dump(plan, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"  - plan.yml: created")

    print("\n" + "=" * 80)
    print("Phases 0-3 completed successfully!")
    print("=" * 80)

    return plan, inputs, existing_mds


if __name__ == "__main__":
    result = main()
