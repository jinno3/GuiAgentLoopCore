# System Constitution

> **GuiAgentLoopCore System Constitution**
> **Version**: 1.0
> **Last Updated**: 2026-02-01T14:53:54.014978+00:00

This document defines the constitutional principles and invariants that govern the GuiAgentLoopCore system. These principles MUST NEVER be violated.

---

## Constitutional Principles

### P1. State Monotonicity Principle
The system state MUST always transition forward. Backward state transitions are prohibited.

**Implementation**: INV-STATE-001
**Rationale**: Ensures system consistency and prevents undefined behavior

### P2. Type Safety Principle
All message types MUST be from the enumerated set. No dynamic type creation is allowed.

**Implementation**: INV-MSG-001
**Rationale**: Prevents runtime errors and ensures predictable message handling

### P3. User Control Principle
Automatic intervention MUST NOT occur during active execution.

**Implementation**: INV-AUTO-001
**Rationale**: Maintains user agency and prevents unexpected system behavior

### P4. Uniqueness Principle
All sessions MUST be uniquely identifiable.

**Implementation**: INV-SESSION-001
**Rationale**: Prevents session collision and ensures correct authentication

### P5. Flexibility Principle
Streaming interfaces MUST support both synchronous and asynchronous patterns.

**Implementation**: INV-STREAM-001
**Rationale**: Enables flexible integration with various client types

---

## Hard Invariants (Constitutional Constraints)

The following invariants have constitutional status and CANNOT be violated:


### INV-STATE-001: Stateは単調遷移する：STATE_INIT → STATE_RUNNING → STATE_STOP

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Interpreter, State

**Rationale**: 状態遷移の一貫性を保証し、不整合な動作を防ぐ

**Constitutional Impact**: 
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-SESSION-001: セッションは一意のUUIDで識別される

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Session

**Rationale**: セッションの衝突を防ぎ、正しい認証を実現する

**Constitutional Impact**: 
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-MSG-001: Messageタイプは定義された列挙型のみ：MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Message

**Rationale**: タイプ安全性を保証し、予期しないMessageを防ぐ

**Constitutional Impact**: 
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-AUTO-001: AutoChatはSTATE_STOP時のみトリガーされる

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: AutoChat, State

**Rationale**: 実行中の自動干渉を防ぎ、ユーザーコントロールを維持する

**Constitutional Impact**: 
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-STREAM-001: ストリームラッパーは同期・非同期の両方をサポートする

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: StreamWrapper, Message

**Rationale**: 柔軟な統合を可能にする

**Constitutional Impact**: 
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


---

## Amendment Process

To amend constitutional invariants:

1. **Proposal**: Submit a proposal with rationale and evidence
2. **Review**: Core maintainers review the impact
3. **Consensus**: Requires unanimous agreement from core maintainers
4. **Documentation**: Update this document and `.concept/invariants.yml`
5. **Testing**: Add tests to verify the new invariant

---

## Enforcement

Constitutional invariants are enforced through:

1. **Code Review**: All PRs MUST pass constitutional review
2. **Automated Tests**: Tests MUST verify all hard invariants
3. **CI/CD**: Automated checks run on every commit
4. **Periodic Audits`: Regular audits of codebase compliance

---

**This constitution is a living document**. Proposals for amendments are welcome but require careful consideration of system-wide impacts.

---

**Related Documents**:
- [AGENTS.md](AGENTS.md) - AI agent behavioral guidelines
- [GLOSSARY.md](GLOSSARY.md) - Terminology definitions
- `.concept/invariants.yml` - Detailed invariant specifications
