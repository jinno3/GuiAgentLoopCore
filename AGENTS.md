# AGENTS.md - AI Agent向け指示

> **プロジェクト**: GuiAgentLoopCore
> **目的**: GUIとLLMエージェントのブリッジとなるコアロジックを提供
> **モード**: concept_driven（.concept/ontology.yml v0.3に基づいて稼働中）

---

## 用語規約（必読）

このリポジトリでは概念の一意性を保つため、以下の正規形を使用します。

| 正規形 | 同義語（使用禁止） | 定義 |
|--------|------------------|------|
| `Interpreter` | GuiAgentInterpreter, 会話インタープリタ | 会話フローとエージェント相互作用を管理する中核コンポーネント |
| `Agent` | AIエージェント, 専門エージェント, AgentType, AgentDefinition, TaskAgent, AgentImage | 特定の役割と実装タイプを持つ専門化AIエンティティ |
| `Session` | ChatSession, 会話セッション, JWT | 一意のIDで管理される会話コンテキスト |
| `Message` | メッセージ, ChatMessage | ユーザー、システム、エージェント間の構造化された通信単位 |
| `State` | InterpreterState, インタープリタ状態 | インタープリタの実行状態を表す列挙型 |
| `AutoChat` | 自動チャット, 自動継続 | STATE_STOP時に自動的に会話を継続する機能 |
| `StreamWrapper` | GuiAgentStreamWrapper, ストリームラッパー | 同期・非同期ストリーミング応答を統一的に扱うユーティリティ |
| `Backend` | GUIバックエンド, UIフレームワーク, GuiBackend, GuiComponent | GUIフレームワーク実装（Gradio等） |
| `Memory` | 会話メモリ, ConversationBuffer | 会話履歴を保持するバッファ機構 |
| `Converter` | 変換器, マッパー | データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ |
| `Connector` | コネクタ, GuiAgentInterpreterABC, ConnectorImplCodeinterpreterApi, ConnectorImplOpenInterpreter | 中核インタープリタと異なるエージェント実装をブリッジする実装固有のアダプタ |

❌ **禁止**: 同義語をコードやドキュメントで使用すること
✅ **必須**: 常に正規形を使用すること

**詳細**: `.concept/ontology.yml`または`GLOSSARY.md`を参照してください。

---

## 不変条件（絶対に破ってはいけない）

以下の**hard invariants**は、システムの安全性と一貫性を保証するため、絶対に違反してはいけません。

### 🔒 状態遷移の単調性
- **INV-STATE-001**: `Interpreter`の状態は単調遷移する：`STATE_INIT` → `STATE_RUNNING` → `STATE_STOP`
  - 状態を逆行させてはいけない（例：`STATE_RUNNING`から`STATE_INIT`へ）
  - 状態遷移の一貫性を保つため、`change_state_running()`等の専用メソッドを使用すること
- **INV-STATE-002**: `State`は3秒間隔のタイマーで自動更新される
  - UI同期と監視を実現するため、`t3 = gr.Timer(3)`で定期更新を行う

### 🔒 Messageタイプの制約
- **INV-MSG-001**: `Message`タイプは定義された列挙型のみ使用可：`MESSAGE`, `CODE`, `CONFIRMATION`, `CONSOLE`, `IMAGE`, `FUNCTION`
  - タイプ安全性を保証するため、`MessageTypeEnum`以外の値を使用しないこと
  - 予期しない`Message`を処理しようとしてはいけない
- **INV-MESSAGE-001**: `Message`は最大100長（MAX_MESSAGE_LENGTH）
  - メモリ使用量を制限し、パフォーマンスを維持するため、メッセージ履歴の長さを制限すること

### 🔒 セッションの一意性とセキュリティ
- **INV-SESSION-001**: `Session`は一意のUUIDで識別される
  - セッションの衝突を防ぐため、UUID生成には標準ライブラリを使用すること
  - 正しい認証を実現するため、セッションIDを適切に管理すること
- **INV-SESSION-002**: セッショントークンはJWTでエンコードされ、HS256アルゴリズムを使用する
  - セキュアなセッション識別と検証を保証するため、jwt.encode()を使用すること

### 🔒 Agentの役割制約
- **INV-AGENT-001**: エージェントは定義された役割を持つ：`AGENT_EXECUTOR`, `LLM_PLANNER`, `SUPERVISOR`, `THOUGHT`, `CREW`, `OTHER`
  - 役割ベースのアクセス制御と責任分離を維持すること

### 🔒 AutoChatの発火条件
- **INV-AUTO-001**: `AutoChat`は`STATE_STOP`時のみトリガーされる
  - 実行中（`STATE_RUNNING`）の自動干渉を防ぐため、状態チェックをトリガー前に行うこと
  - ユーザーコントロールを維持するため、この条件を緩和してはいけない

### 🔒 ストリーム処理の互換性
- **INV-STREAM-001**: `StreamWrapper`は同期・非同期の両方をサポートする
  - 柔軟な統合を可能にするため、両方のケースを考慮した実装を維持すること

### 🔒 Memoryの制約（暫定）
- **INV-MEM-001**: 会話メモリは最大100メッセージまで保持する
  - メモリ使用量を制限し、パフォーマンスを維持するため（draft status）

### 🔒 Connectorのインターフェース制約
- **INV-CONNECTOR-001**: コネクタは必ず`GuiAgentInterpreterABC`インターフェースを実装する
  - 異なる実装間でのインターフェースの一貫性を保証するため

### 🔒 Converterの変換ルール
- **INV-CONVERTER-001**: コンバータは構造化変換のために`MappingRule`を使用する
  - 一貫したデータ変換パターンを保証するため

### 🔒 Backendのセキュリティ
- **INV-BACKEND-001**: バックエンドサーバーは`allowed_paths`でセキュリティ制限される
  - ファイルアクセスを制限し、セキュリティを強化するため
- **INV-BACKEND-002**: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する
  - UIと状態の同期メカニズムを保証するため（3秒間隔）

---

## AUTO決定（暫定仕様）

以下の決定はAUTO決定として記録されており、将来変更される可能性があります。コードを変更する際は、`.concept/ambiguities.yml`を参照してください。

### Agent関連
- **AUTO:Agent.role:classification**: Agentはロールベースで分類される（有効期限：20回の実行）
- **AUTO:Agent.type:implementation_property**: AgentTypeはAgentの実装タイプ別プロパティ（AgentNameの役割とは独立）（有効期限：20回の実行）

### State関連
- **AUTO:State.lifecycle:monotonic**: 状態は単調遷移する（INIT → RUNNING → STOP）（有効期限：20回の実行）
- **AUTO:State.transition:auto_on_input**: ユーザー入力時（textbox.submit）に自動的にRUNNINGに遷移（有効期限：20回の実行）
- **AUTO:State.timer:3sec**: t3タイマーは3秒間隔（有効期限：20回の実行）

### Message関連
- **AUTO:Message.structure:flat**: メッセージは再帰的にフラット化可能（有効期限：20回の実行）
- **AUTO:Message.limit:100**: MAX_MESSAGE_LENGTH=100はハードリミット（有効期限：20回の実行）

### AutoChat関連
- **AUTO:AutoChat.trigger:stop_only**: AutoChatはSTATE_STOP時のみ発火（有効期限：20回の実行）
- **AUTO:AutoChat.prompt:default_continue**: 未設定時はデフォルト継続プロンプト使用（安全側）（有効期限：20回の実行）

### Backend関連
- **AUTO:Backend.primary:gradio**: Gradioが主要`Backend`（暫定）（有効期限：20回の実行）
- **AUTO:Backend.deployment:security**: バックエンドは0.0.0.0で起動し、allowed_pathsでセキュリティ制限（有効期限：20回の実行）

### Memory関連
- **AUTO:Memory.window:k10**: メモリウィンドウサイズはk=10（暫定）（有効期限：20回の実行）
- **AUTO:Memory.specs:provisional**: ウィンドウサイズk=10（rolling）、最大長100（hard limit）（暫定）（有効期限：20回の実行）

### Connector関連
- **AUTO:Connector.layer:domain**: Connectorは正規概念（domain層）（有効期限：20回の実行）

---

## 行動規範

### このリポジトリでやるべきこと

1. **用語の正規形を使用する**
   - コード、ドキュメント、コミット`Message`で常に正規形を使用すること
   - 新しい用語を導入する際は、`.concept/term_queue.yml`を通じて申請すること

2. **不変条件を遵守する**
   - 上記のhard invariantsを理解し、違反するコードを書かないこと
   - 状態遷移、`Message`タイプ、セッション管理に関しては特に注意すること

3. **AUTO決定を尊重する**
   - AUTO決定が適用されている箇所を変更する際は、`.concept/ambiguities.yml`を確認すること
   - 暫定仕様であることを理解し、必要であれば正式な決定を提案すること

4. **概念の一意性を維持する**
   - 同じ概念に対して複数の用語を使用しないこと
   - 曖昧な表現を見つけたら、`.concept/ambiguities.yml`に報告すること

5. **テストを重視する**
   - 不変条件を検証するテストを書くこと
   - 状態遷移、`Message`処理、セッション管理に関するテストカバレッジを維持すること

### このリポジトリでやってはいけないこと

1. ❌ **同義語の使用**: 正規形ではなく同義語を使用すること
2. ❌ **状態遷移の逆行**: `STATE_RUNNING`から`STATE_INIT`へ戻るような状態遷移
3. ❌ **`Message`タイプの無制限追加**: `MessageTypeEnum`に定義されていないタイプを使用すること
4. ❌ **AutoChatの実行中発火**: `STATE_RUNNING`時にAutoChatをトリガーすること
5. ❌ **セッションIDの重複**: UUID以外の方法でセッションを識別すること
6. ❌ **AUTO決定の無視**: 暫定仕様であることを理解せずに変更すること
7. ❌ **用語の重複定義**: 既存の用語と重複する新しい用語を導入すること

---

## 概念辞書との統合

このプロジェクトでは`.concept/ontology.yml`によって管理される概念辞書を使用しています。

- **用語の定義**: `GLOSSARY.md`を参照してください（自動生成）
- **概念のマッピング**: `.concept/mappings.yml`を参照してください
- **不変条件**: `.concept/invariants.yml`を参照してください
- **曖昧性の管理**: `.concept/ambiguities.yml`を参照してください

---

## 開発者向けリソース

### ドキュメント
- `README.md`: プロジェクト概要
- `CONTRIBUTING.md`: 貢献ガイド（必読）
- `GLOSSARY.md`: 用語集（ontology.ymlから自動生成）

### 概念モデル
- `.concept/ontology.yml`: 概念辞書（用語の正規形）
- `.concept/invariants.yml`: 不変条件
- `.concept/ambiguities.yml`: 曖昧性とAUTO決定

### コードベース
- `gui_agent_loop_core/core/interpreter_manager.py`: Interpreterの実装
- `gui_agent_loop_core/schema/`: データスキーマ定義
- `gui_agent_loop_core/converter/`: データ変換ロジック
- `gui_agent_loop_core/backend/`: GUI `Backend`実装

---

**最終更新**: 2026-02-02T13:23:00Z（.concept/ontology.yml v0.3 + invariants.ymlに基づく - verified, no changes needed）
