# AGENTS.md - AIエージェント向け指示

> このリポジトリの存在意義: GuiAgentLoopCore provides the core logic for bridging GUI frameworks and LLM agents, managing conversation flow, agent interactions, and state control.


## 用語規約（必読）

このリポジトリでは概念の一意性を保つため、以下の正規形を使用します。

### コア用語（Core Terms）- 必須

| 正規形 | 同義語（使用禁止） | 定義 |
|--------|------------------|------|
| `Interpreter` | GuiAgentInterpreter, 会話インタープリタ | 会話フローとエージェント相互作用を管理する中核コンポーネント |
| `Agent` | AIエージェント, 専門エージェント, AgentType, AgentDefinition, TaskAgent, AgentImage | 特定の役割と実装タイプを持つ専門化AIエンティティ |
| `Session` | ChatSession, 会話セッション, JWT | 一意のIDで管理される会話コンテキスト（JWT認証使用） |
| `Message` | メッセージ, ChatMessage | ユーザー、システム、エージェント間の構造化された通信単位 |
| `State` | InterpreterState, インタープリタ状態 | インタープリタの実行状態を表す列挙型 |

### ドメイン用語（Domain Terms）

| 正規形 | 同義語（使用禁止） | 定義 |
|--------|------------------|------|
| `AutoChat` | 自動チャット, 自動継続 | STATE_STOP時に自動的に会話を継続する機能 |
| `StreamWrapper` | GuiAgentStreamWrapper, ストリームラッパー | 同期・非同期ストリーミング応答を統一的に扱うユーティリティ |
| `Backend` | GUIバックエンド, UIフレームワーク, GuiBackend, GuiComponent | GUIフレームワーク実装（Gradio等） |
| `Memory` | 会話メモリ, ConversationBuffer | 会話履歴を保持するバッファ機構 (**status: draft**) |
| `Connector` | コネクタ, GuiAgentInterpreterABC, ConnectorImplCodeinterpreterApi, ConnectorImplOpenInterpreter, OpenGuiConnector | 中核インタープリタと異なるエージェント実装をブリッジする実装固有のアダプタ |

### 補助用語（Auxiliary Terms）

| 正規形 | 同義語（使用禁止） | 定義 |
|--------|------------------|------|
| `Converter` | 変換器, マッパー | データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ |

❌ **禁止**: 同義語をコードやドキュメントで使用すること
✅ **必須**: 常に正規形を使用すること

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

#### Hard Invariants（強制不変条件）
これらの不変条件はシステムの正しさと安全性を保証するため、絶対に違反してはなりません。

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

#### Soft Invariants（推奨不変条件）
これらの不変条件はベストプラクティスとして推奨されますが、例外的な状況では緩和される可能性があります。

- ⚠️ **INV-AGENT-001**: エージェントは定義された役割を持つ：AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW, OTHER
- ⚠️ **INV-MEM-001** [DRAFT]: 会話メモリは最大100メッセージまで保持する（Memory機能はdraft状態）
- ⚠️ **INV-BACKEND-002**: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する

## AUTO決定（暫定仕様）

このプロジェクトでは、概念の曖昧性を解決するためにAUTO決定（暫定仕様）を使用しています。これらは証拠に基づいて自動的に決定された仕様ですが、将来的に変更される可能性があります。

### Agent関連のAUTO決定

- **AUTO:Agent.role:classification** - Agentはロールベースで分類される（AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW, OTHER）
- **AUTO:Agent.type:implementation_property** - AgentTypeは実装タイプ別プロパティ（AgentNameの役割とは独立）

### Message関連のAUTO決定

- **AUTO:Message.structure:flat** - メッセージは再帰的にフラット化可能
- **AUTO:Message.limit:100** - MAX_MESSAGE_LENGTH=100はハードリミット
- **AUTO:Message.roles:tool_function_separation** - TOOLとFUNCTIONは異なるセマンティクスを持つ（暫定）

### State関連のAUTO決定

- **AUTO:State.lifecycle:monotonic** - 状態は単調遷移する（INIT → RUNNING → STOP）
- **AUTO:State.transition:auto_on_input** - ユーザー入力時（textbox.submit）に自動的にRUNNINGに遷移
- **AUTO:State.transition:forward_only** - 状態遷移は前方のみ（逆行不可）

### AutoChat関連のAUTO決定

- **AUTO:AutoChat.trigger:stop_only** - AutoChatはSTATE_STOP時のみ発火
- **AUTO:AutoChat.check:before_trigger** - 状態チェックはトリガー前に行われる
- **AUTO:AutoChat.prompt:default_continue** - 未設定時はデフォルト継続プロンプト使用（安全側）

### Backend関連のAUTO決定

- **AUTO:Backend.primary:gradio** - Gradioが主要バックエンド（暫定）
- **AUTO:Backend.deployment:security** - バックエンドは0.0.0.0で起動し、allowed_pathsでセキュリティ制限
- **AUTO:Backend.timer:3sec_interval** - t3タイマーは3秒間隔

### Memory関連のAUTO決定

- **AUTO:Memory.window:k10** - メモリウィンドウサイズはk=10（暫定）
- **AUTO:Memory.limit:100** - 100は安全上限（暫定）
- **AUTO:Memory.specs:provisional** - ウィンドウサイズk=10（rolling）、最大長100（hard limit）（暫定）
- **AUTO:Memory.implementation:dual_provisional** - 両者は暫定的に共存（移行期間中とみなす）

### Session関連のAUTO決定

- **AUTO:Session.jwt:algorithm_hs256** - JWTはHS256アルゴリズム使用（暫定）

### Connector関連のAUTO決定

- **AUTO:Connector.layer:domain** - Connectorは正規概念（domain層）

### Converter関連のAUTO決定

現在、Converterに関連するAUTO決定はありません。

> **重要**: これらのAUTO決定は暫定仕様です。変更する必要がある場合、まず`.concept/ambiguities.yml`を確認し、変更の正当性を説明するevidenceを提供してください。

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

**最終更新**: 2026-02-03T01:11:16Z (bootstrap run v1.1 - run #69 - verified with ontology v0.3, invariants v2026-02-02T05:23:14Z)
