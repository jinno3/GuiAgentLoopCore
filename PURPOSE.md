# Purpose

> **GuiAgentLoopCore Project Purpose**
> **Version**: 1.0

---

## Mission Statement

GuiAgentLoopCore provides the **core logic for bridging GUI frameworks and LLM agents**, managing conversation flow, agent interactions, and state control.

---

## Vision

We envision a world where:

1. **Seamless GUI-LLM Integration**: Any GUI framework can easily integrate with LLM agents
2. **Consistent Behavior**: State management and conversation flow are predictable and reliable
3. **Extensible Architecture**: New agents and backends can be added without modifying core logic
4. **Type Safety**: All operations are type-safe and prevent runtime errors
5. **Clear Semantics**: Every component has well-defined behavior and boundaries

---

## Core Objectives

### O1. Provide Centralized Conversation Management
**Problem**: LLM agent interactions with GUIs are scattered and inconsistent.
**Solution**: `Interpreter` component centralizes conversation flow, state management, and agent coordination.

### O2. Ensure State Consistency
**Problem**: State transitions can be inconsistent, leading to undefined behavior.
**Solution**: Enforce monotonic state transitions (INIT → RUNNING → STOP) through hard invariants.

### O3. Support Multiple Agent Types
**Problem**: Different agents need different interaction patterns.
**Solution**: Role-based agent system (`AGENT_EXECUTOR`, `LLM_PLANNER`, `SUPERVISOR`, etc.) with clear boundaries.

### O4. Enable Flexible Integration
**Problem**: Different GUI frameworks have different interfaces.
**Solution**: Abstract backend interface with pluggable implementations (Gradio, future frameworks).

### O5. Maintain Type Safety
**Problem**: Dynamic message types can cause runtime errors.
**Solution**: Enumerated message types (`MESSAGE`, `CODE`, `CONFIRMATION`, etc.) with strict validation.

---

## What We Do (In Scope)

- **Conversation Flow Management**: Centralize how conversations flow through the system
- **State Machine**: Provide reliable state transitions with monotonic guarantees
- **Agent Coordination**: Manage multiple specialized agents with clear roles
- **Message Processing**: Handle structured communication between users, systems, and agents
- **Backend Abstraction**: Enable multiple GUI framework implementations
- **Streaming Support**: Unified handling of sync and async streaming responses

---

## What We Don't Do (Out of Scope)

- **UI Rendering**: We don't handle UI component rendering (that's the backend's job)
- **LLM Execution**: We don't directly execute LLM models (we delegate to agents)
- **Session Storage**: We don't persist sessions to databases (that's application-level)
- **Authentication**: We don't handle user authentication (we only ensure session uniqueness)
- **Network Protocols**: We don't define network protocols (that's backend-specific)

---

## Target Users

1. **Application Developers**: Building LLM-powered applications with GUI interfaces
2. **AI Agent Developers**: Creating specialized agents for specific tasks
3. **Framework Developers**: Building new GUI backend implementations
4. **AI Agents**: Claude, Gemini, Codex, and other AI models working with this codebase

---

## Success Metrics

We succeed when:

1. **Integration Time**: New applications can integrate GuiAgentLoopCore in < 1 hour
2. **Bug-Free State Transitions**: Zero state transition bugs in production
3. **Agent Compatibility**: New agents can be added without core modifications
4. **Type Safety**: Zero runtime type errors in message handling
5. **Documentation Clarity**: All concepts have unambiguous definitions

---

## Design Philosophy

### P1. Correctness Over Convenience
We prioritize system correctness over developer convenience. Hard invariants cannot be bypassed.

### P2. Explicit Over Implicit
All state transitions, message types, and agent roles are explicitly defined. No magic behavior.

### P3. Small, Focused Components
Each component has a single, well-defined responsibility. Clear boundaries between components.

### P4. Testability
All behavior is testable. Hard invariants have automated tests.

### P5. Conceptual Integrity
All terminology is normalized and defined in a formal ontology. No ambiguity.

---

## Future Direction

### Short-term (0-3 months)
- Complete test coverage for all hard invariants
- Add more backend implementations (beyond Gradio)
- Enhance streaming capabilities

### Medium-term (3-6 months)
- Add session persistence plugins
- Support for streaming state updates
- Performance optimization for high-volume scenarios

### Long-term (6-12 months)
- Multi-interpreter support
- Distributed agent coordination
- Advanced memory management

---

**This purpose document is maintained in sync with**:
- `.concept/ontology.yml` - Formal concept definitions
- `.concept/invariants.yml` - System constraints
- [README.md](README.md) - User-facing overview

---

**Last Updated**: 2026-02-04T08:32:47Z (bootstrap run v1.1 - verified ontology alignment v0.3, run #85)
**Next Review**: 2026-02-04
**Synced With**: `.audit/config/intent.yml` v1.0, `.concept/ontology.yml` v0.3

---

**Note**: This document uses canonical terminology as defined in `.concept/ontology.yml`. All key concepts (`Interpreter`, `Agent`, `Session`, `Message`, `State`) are aligned with the formal ontology. See [GLOSSARY.md](GLOSSARY.md) for complete term definitions.
