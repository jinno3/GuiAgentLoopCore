# 用語集 (Glossary)

> このドキュメントは`.concept/ontology.yml`から自動生成されています。
> 用語の追加・変更は`.concept/term_queue.yml`を通じて行ってください。

**最終更新**: 2026-02-04T05:30:00Z
**Ontologyバージョン**: 0.3
**総用語数**: 11 (Core: 5, Domain: 5, Aux: 1)
**総AUTO決定数**: 16
**総不変条件数**: 14 (Hard: 11, Soft: 3)

---

## コア用語（Core Terms）

プロジェクトの根幹を成す用語。変更には慎重な検討が必要。

### Interpreter

- **定義**: 会話フローとエージェント相互作用を管理する中核コンポーネント
- **同義語**: GuiAgentInterpreter, 会話インタープリタ
- **含む**: 状態管理, セッション管理, メッセージルーティング
- **含まない**: UI描画, LLM直接実行
- **ライフサイクル**: STATE_INIT, STATE_RUNNING, STATE_STOP
- **関連用語**: Agent, Session, Message, State
- **ステータス**: stable

**証拠**:
- `gui_agent_loop_core/core/interpreter_manager.py`: "class InterpreterManager: Manages chat sessions and state handling"

---

### Agent

- **定義**: 特定の役割と実装タイプを持つ専門化AIエンティティ
- **同義語**: AIエージェント, 専門エージェント, AgentType, AgentDefinition, TaskAgent, AgentImage
- **役割**: AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW, OTHER
- **含む**: 役割定義, タスク実行, LLM呼び出し, 実装タイプ（TOOL_CALLING/STRUCTURED_CHAT）
- **含まない**: セッション管理, UI描画
- **関連用語**: Interpreter, AgentName, Message, Backend
- **ステータス**: stable

**AUTO決定**:
- AUTO:Agent.role:classification - Agentはロールベースで分類される
- AUTO:Agent.type:implementation_property - 実装タイプはAgentのプロパティ（AgentNameの役割とは独立）

**証拠**:
- `gui_agent_loop_core/schema/core/schema.py`: "class AgentName(str, Enum): AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW"
- `gui_agent_loop_core/schema/agent/schema.py`: "TOOL_CALLING, STRUCTURED_CHAT"

---

### Session

- **定義**: 一意のIDで管理される会話コンテキスト（JWT認証使用）
- **同義語**: ChatSession, 会話セッション, JWT
- **含む**: メッセージ履歴, セッションID（UUID）, JWTトークン（HS256アルゴリズム）
- **含まない**: UI状態, インタープリタ状態
- **ライフサイクル**: created, active, terminated
- **関連用語**: Interpreter, Message, Agent
- **ステータス**: stable

**AUTO決定**:
- AUTO:Session.jwt:algorithm_hs256 - JWTはHS256アルゴリズム使用（暫定）

**証拠**:
- `gui_agent_loop_core/core/interpreter_manager.py`: "ChatSession: Individual conversation session with message history; jwt.encode(session_id, self.secret_key, algorithm='HS256')"

---

### Message

- **定義**: ユーザー、システム、エージェント間の構造化された通信単位
- **同義語**: メッセージ, ChatMessage
- **含む**: コンテンツ, 役割, タイプ, メタデータ, 最大長制限（MAX_MESSAGE_LENGTH=100）
- **含まない**: セッション状態, UIイベント
- **ライフサイクル**: created, processed, streamed
- **関連用語**: Interpreter, Agent, Session
- **ステータス**: stable

**AUTO決定**:
- AUTO:Message.structure:flat - メッセージは再帰的にフラット化可能
- AUTO:Message.limit:100 - MAX_MESSAGE_LENGTH=100はハードリミット
- AUTO:Message.roles:tool_function_separation - TOOLとFUNCTIONは異なるセマンティクスを持つ（暫定）

**証拠**:
- `gui_agent_loop_core/schema/message/schema.py`: "MessageTypeEnum: MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION"
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "MAX_MESSAGE_LENGTH = 100"

---

### State

- **定義**: インタープリタの実行状態を表す列挙型
- **同義語**: InterpreterState, インタープリタ状態
- **含む**: 状態遷移, 状態チェック, 状態変更イベント, タイマーベースの定期更新（3秒間隔）
- **含まない**: セッションライフサイクル, UI状態
- **ライフサイクル**: STATE_INIT, STATE_RUNNING, STATE_STOP
- **関連用語**: Interpreter, AutoChat, Timer
- **ステータス**: stable

**AUTO決定**:
- AUTO:State.lifecycle:monotonic - 状態は単調遷移する（INIT → RUNNING → STOP）
- AUTO:State.transition:auto_on_input - ユーザー入力時（textbox.submit）に自動的にRUNNINGに遷移
- AUTO:State.timer:3sec - t3タイマーは3秒間隔

**証拠**:
- `gui_agent_loop_core/schema/core/schema.py`: "class InterpreterState(str, Enum): STATE_INIT, STATE_RUNNING, STATE_STOP"
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "t3.tick(interpreter_manager.update_state_view, outputs=[agent_state])"
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "chat_iface.textbox.submit(fn=interpreter_manager.change_state_running, outputs=[agent_state])"

---

## ドメイン用語（Domain Terms）

プロジェクトのドメイン特有の用語。

### AutoChat

- **定義**: STATE_STOP時に自動的に会話を継続する機能
- **同義語**: 自動チャット, 自動継続
- **含む**: 自動入力生成, 状態チェック, 継続トリガー
- **含まない**: 手動チャット, UIイベントハンドリング
- **ライフサイクル**: triggered, executed, completed
- **関連用語**: Interpreter, State, Message
- **ステータス**: stable

**AUTO決定**:
- AUTO:AutoChat.trigger:stop_only - AutoChatはSTATE_STOP時のみ発火
- AUTO:AutoChat.prompt:default_continue - 未設定時はデフォルト継続プロンプト使用（安全側）

**証拠**:
- `gui_agent_loop_core/core/interpreter_manager.py`: "auto_chat(): Only triggers when state is STATE_STOP"

---

### StreamWrapper

- **定義**: 同期・非同期ストリーミング応答を統一的に扱うユーティリティ
- **同義語**: GuiAgentStreamWrapper, ストリームラッパー
- **含む**: ストリーム処理, 同期/非同期変換
- **含まない**: メッセージ変換, 状態管理
- **ライフサイクル**: created, streaming, completed
- **関連用語**: Message, Interpreter
- **ステータス**: stable

**証拠**:
- `gui_agent_loop_core/util/gui_agent_stream_wrapper.py`: "GuiAgentStreamWrapper: Utility for handling both sync and async streaming responses"

---

### Backend

- **定義**: GUIフレームワーク実装（Gradio等）
- **同義語**: GUIバックエンド, UIフレームワーク, GuiBackend, GuiComponent
- **含む**: UI描画, イベントハンドリング, コンポーネント管理, GuiComponent列挙, GuiBackendType列挙（GRADIO/STREAMSYNC）
- **含まない**: 会話ロジック, エージェント管理
- **関連用語**: Interpreter, Session, GuiComponent
- **ステータス**: stable

**AUTO決定**:
- AUTO:Backend.primary:gradio - Gradioが主要バックエンド（暫定）
- AUTO:Backend.deployment:security - バックエンドは0.0.0.0で起動し、allowed_pathsでセキュリティ制限
- AUTO:Backend.timer:3sec_interval - 3秒タイマーは妥当な更新頻度（暫定）

**証拠**:
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "Gradio implementation of the server interface"
- `gui_agent_loop_core/schema/backend/schema.py`: "class GuiBackendType(str, enum.Enum): GRADIO, STREAMSYNC"
- `gui_agent_loop_core/schema/backend/schema.py`: "class GuiComponentName(str, enum.Enum): AGENT_NAME, AGENT_NAME_RADIO, AGENT_IMAGE, AGENT_STATE, AGENT_SESSION, CHATBOT, INPUT_TEXTBOX, CHAT_IFACE, OUTPUT_BLOCK"
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "app.launch(server_name='0.0.0.0', debug=True, allowed_paths=['/tmp', '/app/work', '/home', '/app/GuiAgentLoopCore'])"

---

### Memory

- **定義**: 会話履歴を保持するバッファ機構
- **同義語**: 会話メモリ, ConversationBuffer
- **含む**: メッセージ履歴, ウィンドウサイズ
- **含まない**: セッション管理, 状態保持
- **関連用語**: Session, Message
- **ステータス**: draft

**AUTO決定**:
- AUTO:Memory.window:k10 - メモリウィンドウサイズはk=10（暫定）
- AUTO:Memory.specs:provisional - ウィンドウサイズk=10（rolling）、最大長100（hard limit）（暫定）
- AUTO:Memory.limit:100 - 100は安全上限（暫定）
- AUTO:Memory.implementation:dual_provisional - 両者は暫定的に共存（移行期間中とみなす）

**証拠**:
- exploration findings: "Conversation buffer with window size (k=10)"

---

### Connector

- **定義**: 中核インタープリタと異なるエージェント実装をブリッジする実装固有のアダプタ
- **同義語**: コネクタ, GuiAgentInterpreterABC, ConnectorImplCodeinterpreterApi, ConnectorImplOpenInterpreter, OpenGuiConnector
- **含む**: GuiAgentInterpreterABCインターフェースの実装, エージェント固有のブリッジロジック, I/O変換
- **含まない**: UI描画, LLM直接実行, セッション管理
- **ライフサイクル**: initialized, connected, executing, disconnected
- **関連用語**: Interpreter, Agent
- **ステータス**: stable

**AUTO決定**:
- AUTO:Connector.layer:domain - Connectorは正規概念（domain層）

**証拠**:
- `gui_agent_loop_core/connector_impl/core_to_agent/connector_impl_codeinterpreter_api.py`: "class ConnectorImplCodeinterpreterApi(GuiAgentInterpreterABC)"
- `gui_agent_loop_core/connector_impl/core_to_agent/connector_impl_open_interpreter.py`: "class ConnectorImplOpenInterpreter(GuiAgentInterpreterABC)"
- `gui_agent_loop_core/schema/core/schema.py`: "class GuiAgentInterpreterABC(ABC): Abstract interface for agent connectors"

---

## 補助用語（Auxiliary Terms）

ユーティリティやサポート機能の用語。

### Converter

- **定義**: データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ
- **同義語**: 変換器, マッパー
- **含む**: リクエスト変換, 辞書フラット化, コードコンテンツ処理, format/languageフィールド抽出
- **含まない**: メッセージ処理, 状態管理
- **ライフサイクル**: created, converting, flattened
- **関連用語**: Message
- **ステータス**: stable

**証拠**:
- `gui_agent_loop_core/converter/request_converter.py`: "RequestConverter handles code content by extracting format and language fields, flattens nested content recursively"

---

## 用語の正規化マップ

以下の同義語は、必ず上記の正規形に置き換えて使用してください。

| 同義語 | 正規形 |
|--------|--------|
| GuiAgentInterpreter | Interpreter |
| 会話インタープリタ | Interpreter |
| AIエージェント | Agent |
| 専門エージェント | Agent |
| AgentType | Agent |
| AgentDefinition | Agent |
| TaskAgent | Agent |
| AgentImage | Agent |
| ChatSession | Session |
| 会話セッション | Session |
| メッセージ | Message |
| ChatMessage | Message |
| InterpreterState | State |
| インタープリタ状態 | State |
| 自動チャット | AutoChat |
| 自動継続 | AutoChat |
| GuiAgentStreamWrapper | StreamWrapper |
| ストリームラッパー | StreamWrapper |
| GUIバックエンド | Backend |
| UIフレームワーク | Backend |
| GuiBackend | Backend |
| GuiComponent | Backend |
| 会話メモリ | Memory |
| ConversationBuffer | Memory |
| 変換器 | Converter |
| マッパー | Converter |
| コネクタ | Connector |
| GuiAgentInterpreterABC | Connector |
| ConnectorImplCodeinterpreterApi | Connector |
| ConnectorImplOpenInterpreter | Connector |

---

**生成元**: `.concept/ontology.yml` (v0.3, updated: 2026-02-03T12:21:29Z)
**生成日時**: 2026-02-04T05:30:00Z
**担当**: 16_repo_md_bootstrapper v1.1 (audit + concept統合 - run #81)

---

## 関連ドキュメント

- **用語の正規形と定義**: `.concept/ontology.yml`
- **不変条件**: `.concept/invariants.yml` (14件の不変条件)
- **AUTO決定（暫定仕様）**: `.concept/ambiguities.yml` (9件の ambiguity、16件のAUTO決定)
- **用語追加リクエスト**: `.concept/term_queue.yml`

---

## 不変条件の概要

このプロジェクトでは以下の14件の不変条件を定義しています：

### Hard Invariants (11件) - 違反が厳密に禁止される条件

- **INV-STATE-001**: インタープリタ状態は単調遷移する（STATE_INIT → STATE_RUNNING → STATE_STOP）
- **INV-SESSION-001**: セッションは一意のUUIDで識別される
- **INV-MSG-001**: メッセージタイプは定義された列挙型のみ
- **INV-AUTO-001**: AutoChatはSTATE_STOP時のみトリガーされる
- **INV-STREAM-001**: ストリームラッパーは同期・非同期の両方をサポートする
- **INV-MESSAGE-001**: メッセージは最大100長（MAX_MESSAGE_LENGTH）
- **INV-STATE-002**: 状態は3秒間隔のタイマーで自動更新される
- **INV-BACKEND-001**: バックエンドサーバーはallowed_pathsでセキュリティ制限される
- **INV-SESSION-002**: セッショントークンはJWTでエンコードされ、HS256アルゴリズムを使用する
- **INV-CONNECTOR-001**: コネクタは必ずGuiAgentInterpreterABCインターフェースを実装する
- **INV-CONVERTER-001**: コンバータは構造化変換のためにMappingRuleを使用する

### Soft Invariants (3件) - 推奨されるが例外的な状況があり得る条件

- **INV-AGENT-001**: エージェントは定義された役割を持つ
- **INV-MEM-001**: 会話メモリは最大100メッセージまで保持する（draft）
- **INV-BACKEND-002**: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する

詳細は `.concept/invariants.yml` を参照してください。

---

## AUTO決定（暫定仕様）について

このプロジェクトには**16件のアクティブなAUTO決定**があります。これらは`.concept/ambiguities.yml`に記録されており、暫定仕様として扱われます。

主なAUTO決定：
- **Agent**: AUTO:Agent.role:classification, AUTO:Agent.type:implementation_property
- **Message**: AUTO:Message.structure:flat, AUTO:Message.limit:100, AUTO:Message.roles:tool_function_separation
- **State**: AUTO:State.lifecycle:monotonic, AUTO:State.transition:auto_on_input, AUTO:State.timer:3sec
- **AutoChat**: AUTO:AutoChat.trigger:stop_only, AUTO:AutoChat.prompt:default_continue
- **Backend**: AUTO:Backend.primary:gradio, AUTO:Backend.deployment:security, AUTO:Backend.timer:3sec_interval
- **Memory**: AUTO:Memory.window:k10, AUTO:Memory.specs:provisional, AUTO:Memory.limit:100, AUTO:Memory.implementation:dual_provisional
- **Session**: AUTO:Session.jwt:algorithm_hs256
- **Connector**: AUTO:Connector.layer:domain

詳細は `.concept/ambiguities.yml` を参照してください。
