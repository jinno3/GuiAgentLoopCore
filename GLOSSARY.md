# 用語集 (Glossary)

> このドキュメントは`.concept/ontology.yml`から自動生成されています。
> 用語の追加・変更は`.concept/term_queue.yml`を通じて行ってください。

**最終更新**: 2026-02-01T13:05:48Z
**Ontologyバージョン**: 0.3
**総用語数**: 9

---

## コア用語（Core Terms）

プロジェクトの根幹を成す用語。変更には慎重な検討が必要。

### Interpreter

- **定義**: 会話フローとエージェント相互作用を管理する中核コンポーネント
- **同義語**: GuiAgentInterpreter, 会話インタープリタ（使用禁止）
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
- **同義語**: AIエージェント, 専門エージェント（使用禁止）
- **含む**: 役割定義, タスク実行, LLM呼び出し, 実装タイプ（TOOL_CALLING/STRUCTURED_CHAT）
- **含まない**: セッション管理, UI描画
- **関連用語**: Interpreter, AgentName, Message, AgentType
- **ステータス**: stable

**AUTO決定**:
- AUTO:Agent.role:classification - Agentはロールベースで分類される
- AUTO:Agent.type:implementation_property - AgentTypeはAgentの実装タイプ別プロパティ（AgentNameの役割とは独立）

**証拠**:
- `gui_agent_loop_core/schema/core/schema.py`: "class AgentName(str, Enum): AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW"
- `gui_agent_loop_core/schema/agent/schema.py`: "class AgentType(str, enum.Enum): TOOL_CALLING, STRUCTURED_CHAT"

---

### Session

- **定義**: 一意のIDで管理される会話コンテキスト
- **同義語**: ChatSession, 会話セッション（使用禁止）
- **含む**: メッセージ履歴, セッションID, 認証トークン
- **含まない**: UI状態, インタープリタ状態
- **ライフサイクル**: created, active, terminated
- **関連用語**: Interpreter, Message, ChatManager
- **ステータス**: stable

**証拠**:
- `gui_agent_loop_core/core/interpreter_manager.py`: "ChatSession: Individual conversation session with message history"

---

### Message

- **定義**: ユーザー、システム、エージェント間の構造化された通信単位
- **同義語**: メッセージ, ChatMessage（使用禁止）
- **含む**: コンテンツ, 役割, タイプ, メタデータ
- **含まない**: セッション状態, UIイベント
- **ライフサイクル**: created, processed, streamed
- **関連用語**: Interpreter, Agent, Session
- **ステータス**: stable

**AUTO決定**:
- AUTO:Message.structure:flat - メッセージは再帰的にフラット化可能

**証拠**:
- `gui_agent_loop_core/schema/message/schema.py`: "MessageTypeEnum: MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION"

---

### State

- **定義**: インタープリタの実行状態を表す列挙型
- **同義語**: InterpreterState, インタープリタ状態（使用禁止）
- **含む**: 状態遷移, 状態チェック, 状態変更イベント
- **含まない**: セッションライフサイクル, UI状態
- **ライフサイクル**: STATE_INIT, STATE_RUNNING, STATE_STOP
- **関連用語**: Interpreter, AutoChat
- **ステータス**: stable

**AUTO決定**:
- AUTO:State.lifecycle:monotonic - 状態は単調遷移する（INIT → RUNNING → STOP）

**証拠**:
- `gui_agent_loop_core/schema/core/schema.py`: "class InterpreterState(str, Enum): STATE_INIT, STATE_RUNNING, STATE_STOP"

---

## ドメイン用語（Domain Terms）

プロジェクトのドメイン特有の用語。

### AutoChat

- **定義**: STATE_STOP時に自動的に会話を継続する機能
- **同義語**: 自動チャット, 自動継続（使用禁止）
- **含む**: 自動入力生成, 状態チェック, 継続トリガー
- **含まない**: 手動チャット, UIイベントハンドリング
- **ライフサイクル**: triggered, executed, completed
- **関連用語**: Interpreter, State, Message
- **ステータス**: stable

**AUTO決定**:
- AUTO:AutoChat.trigger:stop_only - AutoChatはSTATE_STOP時のみ発火

**証拠**:
- `gui_agent_loop_core/core/interpreter_manager.py`: "auto_chat(): Only triggers when state is STATE_STOP"

---

### StreamWrapper

- **定義**: 同期・非同期ストリーミング応答を統一的に扱うユーティリティ
- **同義語**: GuiAgentStreamWrapper, ストリームラッパー（使用禁止）
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
- **同義語**: GUIバックエンド, UIフレームワーク（使用禁止）
- **含む**: UI描画, イベントハンドリング, コンポーネント管理
- **含まない**: 会話ロジック, エージェント管理
- **関連用語**: Interpreter, Session
- **ステータス**: stable

**AUTO決定**:
- AUTO:Backend.primary:gradio - Gradioが主要バックエンド（暫定）

**証拠**:
- `gui_agent_loop_core/backend/server_impl_gradio.py`: "Gradio implementation of the server interface"

---

### Memory

- **定義**: 会話履歴を保持するバッファ機構
- **同義語**: 会話メモリ, ConversationBuffer（使用禁止）
- **含む**: メッセージ履歴, ウィンドウサイズ
- **含まない**: セッション管理, 状態保持
- **関連用語**: Session, Message
- **ステータス**: draft

**AUTO決定**:
- AUTO:Memory.window:k10 - メモリウィンドウサイズはk=10（暫定）

**証拠**:
- exploration findings: "Conversation buffer with window size (k=10)"

---

## 補助用語（Auxiliary Terms）

ユーティリティやサポート機能の用語。

### Converter

- **定義**: データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ
- **同義語**: 変換器, マッパー（使用禁止）
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
| 会話メモリ | Memory |
| ConversationBuffer | Memory |
| 変換器 | Converter |
| マッパー | Converter |

---

**生成元**: `.concept/ontology.yml` (v0.3)
**生成日時**: 2026-02-01T22:09:00Z
**担当**: 16_repo_md_bootstrapper
