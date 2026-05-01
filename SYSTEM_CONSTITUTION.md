# System Constitution

> **GuiAgentLoopCore System Constitution**
> **Version**: 1.1
> **Last Updated**: 2026-05-02T00:30:00Z (bootstrap run v1.1 - all 14 invariants verified with ontology v0.3)

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


### INV-STREAM-001: `StreamWrapper`は同期・非同期の両方をサポートする

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: StreamWrapper, Message

**Rationale**: 柔軟な統合を可能にする

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-MESSAGE-001: `Message`は最大100長（MAX_MESSAGE_LENGTH）

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Message

**Rationale**: メモリ使用量を制限し、パフォーマンスを維持する

**AUTO Decision**: AUTO:Message.limit:100（暫定仕様）

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-STATE-002: 状態は3秒間隔のタイマーで自動更新される

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: State, Timer

**Rationale**: UI同期と監視を実現する

**AUTO Decision**: AUTO:State.timer:3sec（暫定仕様）

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-BACKEND-001: バックエンドサーバーはallowed_pathsでセキュリティ制限される

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Backend

**Rationale**: ファイルアクセスを制限し、セキュリティを強化する

**AUTO Decision**: AUTO:Backend.deployment:security（暫定仕様）

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-SESSION-002: セッショントークンはSessionでエンコードされ、HS256アルゴリズムを使用する

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Session

**Rationale**: セキュアなセッション識別と検証を保証する

**AUTO Decision**: AUTO:Session.jwt:algorithm_hs256（暫定仕様）

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-CONNECTOR-001: Connectorは必ずInterpreterABCインターフェースを実装する

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Connector

**Rationale**: 異なる実装間でのインターフェースの一貫性を保証する

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained


### INV-CONVERTER-001: コンバータは構造化変換のためにMappingRuleを使用する

**Strength**: HARD (Constitutional)
**Status**: stable
**Related Terms**: Converter

**Rationale**: 一貫したデータ変換パターンを保証する

**Constitutional Impact**:
- Violating this invariant compromises system safety
- Changes require constitutional amendment (consensus from maintainers)
- Tests MUST verify this invariant is maintained




### INV-AGENT-001: エージェントは定義された役割を持つ：AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW, OTHER

**Strength**: SOFT (Recommended)
**Status**: stable
**Related Terms**: Agent

**Rationale**: 役割ベースのアクセス制御と責任分離

**AUTO Decision**: AUTO:Agent.role:other_default（暫定仕様）


### INV-MEM-001: 会話メモリは最大100メッセージまで保持する

**Strength**: SOFT (Recommended)
**Status**: draft
**Related Terms**: Memory, Session

**Rationale**: メモリ使用量を制限し、パフォーマンスを維持する

**AUTO Decision**: AUTO:Memory.limit:100（暫定仕様）


### INV-BACKEND-002: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する

**Strength**: SOFT (Recommended)
**Status**: stable
**Related Terms**: Backend, State

**Rationale**: UIと状態の同期メカニズムを保証する

**AUTO Decision**: AUTO:Backend.timer:3sec_interval（暫定仕様）


---

## Soft Invariants (Recommended)

The following invariants are recommended best practices. Exceptions may be allowed under specific circumstances with documented justification.

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
4. **Periodic Audits**: Regular audits of codebase compliance

---

**This constitution is a living document**. Proposals for amendments are welcome but require careful consideration of system-wide impacts.

---

**Related Documents**:
- [AGENTS.md](AGENTS.md) - AI agent behavioral guidelines
- [GLOSSARY.md](GLOSSARY.md) - Terminology definitions
- `.concept/invariants.yml` - Detailed invariant specifications
