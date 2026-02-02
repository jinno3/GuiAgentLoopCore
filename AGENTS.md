# AGENTS.md - AIエージェント向け指示

> このリポジトリの存在意義: GuiAgentLoopCore provides the core logic for bridging GUI frameworks and LLM agents, managing conversation flow, agent interactions, and state control.


## 用語規約（必読）

このリポジトリでは概念の一意性を保つため、以下の正規形を使用します。

詳細は `GLOSSARY.md` または `.concept/ontology.yml` を参照してください。

## 行動規範

### このリポジトリでやるべきこと

- Centralized Conversation Management: Interpreter component centralizes conversation flow, state management, and agent coordination
- State Machine with Monotonic Transitions: Enforce monotonic state transitions (INIT → RUNNING → STOP) through hard invariants
- Multi-Agent Coordination: Role-based agent system (AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, etc.) with clear boundaries
- Structured Message Processing: Handle structured communication between users, systems, and agents
- Backend Abstraction: Enable multiple GUI framework implementations (Gradio, extensible to others)

### このリポジトリでやってはいけないこと

- ❌ UI Rendering: We don't handle UI component rendering (that's the backend's job)
- ❌ LLM Execution: We don't directly execute LLM models (we delegate to agents)
- ❌ Session Storage: We don't persist sessions to databases (that's application-level)
- ❌ Authentication: We don't handle user authentication (we only ensure session uniqueness)
- ❌ Network Protocols: We don't define network protocols (that's backend-specific)

### 不変条件（絶対に破ってはいけない）

- 🔒 **INV-STATE-001**: インタープリタ状態は単調遷移する：STATE_INIT → STATE_RUNNING → STATE_STOP
- 🔒 **INV-SESSION-001**: セッションは一意のUUIDで識別される
- 🔒 **INV-MSG-001**: メッセージタイプは定義された列挙型のみ：MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION
- 🔒 **INV-AUTO-001**: AutoChatはSTATE_STOP時のみトリガーされる
- 🔒 **INV-STREAM-001**: ストリームラッパーは同期・非同期の両方をサポートする
- 🔒 **INV-MESSAGE-001**: メッセージは最大100長（MAX_MESSAGE_LENGTH）
- 🔒 **INV-STATE-002**: 状態は3秒間隔のタイマーで自動更新される
- 🔒 **INV-BACKEND-001**: バックエンドサーバーはallowed_pathsでセキュリティ制限される
- 🔒 **INV-SESSION-002**: セッショントークンはJWTでエンコードされ、HS256アルゴリズムを使用する
- 🔒 **INV-CONNECTOR-001**: コネクタは必ずGuiAgentInterpreterABCインターフェースを実装する
- 🔒 **INV-CONVERTER-001**: コンバータは構造化変換のためにMappingRuleを使用する

## 開発ガイドライン

### コードを書く際の注意点

1. **状態遷移の単調性**: インタープリタ状態は常に単調遷移する (STATE_INIT → STATE_RUNNING → STATE_STOP)
2. **メッセージタイプ**: 定義された列挙型のみ使用する
3. **型安全性**: すべてのデータ構造は型定義に従う

### テスト

\`\`\`bash
make test
\`\`\`

### ドキュメントの更新

- 用語を追加する際は `.concept/term_queue.yml` を使用
- 不変条件を変更する際は `.concept/invariants.yml` を更新

## 関連ドキュメント

- [CLAUDE.md](CLAUDE.md) - Claude向け特化指示
- [GLOSSARY.md](GLOSSARY.md) - 用語集
- [CONTRIBUTING.md](CONTRIBUTING.md) - 貢献ガイド

---

**最終更新**: 2026-02-02T12:21:43.186425Z
