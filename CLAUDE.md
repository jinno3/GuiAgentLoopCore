# CLAUDE.md - Claude向け特化指示

> プロジェクト: GuiAgentLoopCore
> 対象AIモデル: Claude (Anthropic)

このドキュメントは、Claudeがこのリポジトリで作業する際に従うべき特化指示を提供します。

---

## Claude固有の推奨事項

### 1. 用語の一貫性

Claudeは、このリポジトリの`.concept/ontology.yml`で定義された正規形を優先的に使用します。

#### コア用語（Core Terms）
- `Interpreter` - 会話フローとエージェント相互作用を管理する中核コンポーネント
- `Agent` - 特定の役割と実装タイプを持つ専門化AIエンティティ
- `Session` - 一意のIDで管理される会話コンテキスト
- `Message` - ユーザー、システム、エージェント間の構造化された通信単位
- `State` - インタープリタの実行状態を表す列挙型

#### ドメイン用語（Domain Terms）
- `AutoChat` - STATE_STOP時に自動的に会話を継続する機能
- `StreamWrapper` - 同期・非同期ストリーミング応答を統一的に扱うユーティリティ
- `Backend` - GUIフレームワーク実装（Gradio等）
- `Memory` - 会話履歴を保持するバッファ機構（**status: draft**）
- `Connector` - 中核インタープリタと異なるエージェント実装をブリッジする実装固有のアダプタ

#### 補助用語（Auxiliary Terms）
- `Converter` - データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ

用語の完全なリストは[GLOSSARY.md](GLOSSARY.md)を参照してください。

このプロジェクトには**11個の正規用語**が定義されています：
- **Core (5)**: Interpreter, Agent, Session, Message, State
- **Domain (5)**: AutoChat, StreamWrapper, Backend, Memory, Connector
- **Auxiliary (1)**: Converter

### 2. 不変条件の遵守

Claudeは、以下のhard invariantsを絶対に違反しません：

#### 状態管理（State Management）
- **INV-STATE-001**: インタープリタ状態は単調遷移する：STATE_INIT → STATE_RUNNING → STATE_STOP
  - 状態の逆行は禁止（例：STATE_RUNNING → STATE_INIT）
  - 専用メソッド（`change_state_running()`等）を使用する

```python
# 良い例: 状態遷移の単調性を尊重
def change_state_running(interpreter: Interpreter):
    if interpreter.state == State.STATE_INIT:
        interpreter.state = State.STATE_RUNNING
    else:
        raise InvalidStateTransitionError(
            f"Cannot transition to RUNNING from {interpreter.state}"
        )

# 悪い例: 状態の逆行
def revert_to_init(interpreter: Interpreter):  # ❌ 違反
    interpreter.state = State.STATE_INIT
```

- **INV-STATE-002**: 状態は3秒間隔のタイマーで自動更新される
  - UI同期と監視を実現するための仕様

#### メッセージ処理（Message Processing）
- **INV-MSG-001**: メッセージタイプは定義された列挙型のみ使用
  - 許可されるタイプ: MESSAGE, CODE, CONFIRMATION, CONSOLE, IMAGE, FUNCTION
  - タイプ安全性を保証し、予期しないメッセージ処理を防ぐ

- **INV-MESSAGE-001**: メッセージは最大100長（MAX_MESSAGE_LENGTH）
  - メモリ使用量を制限し、パフォーマンスを維持する
  - **AUTO決定**: AUTO:Message.limit:100（暫定仕様）

#### セッション管理（Session Management）
- **INV-SESSION-001**: セッションは一意のUUIDで識別される
  - セッションの衝突を防ぎ、正しい認証を実現する

- **INV-SESSION-002**: セッショントークンはJWTでエンコードされ、HS256アルゴリズムを使用する
  - セキュアなセッション識別と検証を保証する
  - **AUTO決定**: AUTO:Session.jwt:algorithm_hs256（暫定仕様）

#### エージェント管理（Agent Management）
- **INV-AGENT-001** [soft]: エージェントは定義された役割を持つ
  - 許可される役割: AGENT_EXECUTOR, LLM_PLANNER, SUPERVISOR, THOUGHT, CREW, OTHER
  - 役割ベースのアクセス制御と責任分離
  - **AUTO決定**: AUTO:Agent.role:classification（暫定仕様）

#### AutoChat（AutoChat）
- **INV-AUTO-001**: AutoChatはSTATE_STOP時のみトリガーされる
  - 実行中の自動干渉を防ぎ、ユーザーコントロールを維持する
  - **AUTO決定**: AUTO:AutoChat.trigger:stop_only（暫定仕様）

#### ストリーミング（Streaming）
- **INV-STREAM-001**: ストリームラッパーは同期・非同期の両方をサポートする
  - 柔軟な統合を可能にする

#### バックエンド（Backend）
- **INV-BACKEND-001**: バックエンドサーバーはallowed_pathsでセキュリティ制限される
  - ファイルアクセスを制限し、セキュリティを強化する
  - **AUTO決定**: AUTO:Backend.deployment:security（暫定仕様）

- **INV-BACKEND-002**: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する
  - UIと状態の同期メカニズムを保証する
  - **AUTO決定**: AUTO:Backend.timer:3sec_interval（暫定仕様）

#### メモリ管理（Memory Management）
- **INV-MEM-001**: 会話メモリは最大100メッセージまで保持する
  - メモリ使用量を制限し、パフォーマンスを維持する
  - **AUTO決定**: AUTO:Memory.limit:100（暫定仕様）

#### コネクタ管理（Connector Management）
- **INV-CONNECTOR-001**: コネクタは必ずGuiAgentInterpreterABCインターフェースを実装する
  - 異なる実装間でのインターフェースの一貫性を保証する

#### コンバータ管理（Converter Management）
- **INV-CONVERTER-001**: コンバータは構造化変換のためにMappingRuleを使用する
  - 一貫したデータ変換パターンを保証する

### 3. AUTO決定の認識

Claudeは、AUTO決定（`.concept/ambiguities.yml`に記録）を暫定仕様として扱います。

#### Agent関連のAUTO決定
- **AUTO:Agent.role:classification** - Agentはロールベースで分類される
- **AUTO:Agent.type:implementation_property** - AgentTypeは実装タイプ別プロパティ（AgentNameの役割とは独立）

#### Message関連のAUTO決定
- **AUTO:Message.structure:flat** - メッセージは再帰的にフラット化可能
- **AUTO:Message.limit:100** - MAX_MESSAGE_LENGTH=100はハードリミット
- **AUTO:Message.roles:tool_function_separation** - TOOLとFUNCTIONは異なるセマンティクスを持つ（暫定）

#### State関連のAUTO決定
- **AUTO:State.lifecycle:monotonic** - 状態は単調遷移する（INIT → RUNNING → STOP）
- **AUTO:State.transition:auto_on_input** - ユーザー入力時（textbox.submit）に自動的にRUNNINGに遷移
- **AUTO:State.timer:3sec** - t3タイマーは3秒間隔

#### AutoChat関連のAUTO決定
- **AUTO:AutoChat.trigger:stop_only** - AutoChatはSTATE_STOP時のみ発火
- **AUTO:AutoChat.prompt:default_continue** - 未設定時はデフォルト継続プロンプト使用（安全側）

#### Backend関連のAUTO決定
- **AUTO:Backend.primary:gradio** - Gradioが主要バックエンド（暫定）
- **AUTO:Backend.deployment:security** - バックエンドは0.0.0.0で起動し、allowed_pathsでセキュリティ制限

#### Memory関連のAUTO決定
- **AUTO:Memory.window:k10** - メモリウィンドウサイズはk=10（暫定）
- **AUTO:Memory.specs:provisional** - ウィンドウサイズk=10（rolling）、最大長100（hard limit）（暫定）
- **AUTO:Memory.limit:100** - 100は安全上限（暫定）
- **AUTO:Memory.implementation:dual_provisional** - 両者は暫定的に共存（移行期間中とみなす）

#### Session関連のAUTO決定
- **AUTO:Session.jwt:algorithm_hs256** - JWTはHS256アルゴリズム使用（暫定）

#### Connector関連のAUTO決定
- **AUTO:Connector.layer:domain** - Connectorは正規概念（domain層）

> **注意**: これらは主要なAUTO決定です。全16個のAUTO決定については`.concept/ontology.yml`を参照してください。

### 4. ステートフルな操作の注意

Claudeは、以下のステートフルな操作で特に注意を払います：

- **State管理**: 状態遷移は常に単調的（STATE_INIT → STATE_RUNNING → STATE_STOP）
  - 状態チェックはトリガー前に行う（AUTO:AutoChat.check:before_trigger）
  - タイマーベースの定期更新（3秒間隔）

- **Session管理**: セッションIDはUUIDで一意に
  - セッションの衝突を防ぐ

- **Message処理**: Messageタイプは列挙型のみ使用
  - 最大長制限（MAX_MESSAGE_LENGTH=100）を尊重する
  - メッセージは再帰的にフラット化可能

- **Memory管理**: 会話メモリはdraft状態
  - ウィンドウサイズk=10（rolling）
  - 最大長100（hard limit）
  - 仕様は変更される可能性があるため、注意深く扱う

### 5. Claude特有の強みを活かす

Claudeの以下の特性を活かして、このプロジェクトに貢献してください：

1. **長いコンテキストの理解**: 11個の canonical terms (`Interpreter`、`Agent`、`Session`、`Message`、`State`、`AutoChat`、`StreamWrapper`、`Backend`、`Converter`、`Memory`、`Connector`) の複雑な相互作用を理解
2. **詳細な分析**: 不変条件違反の可能性を詳細に分析
3. **明確な説明**: 技術的な決定を明確に説明し、evidenceを提供
4. **AUTO決定の追跡**: 16個のアクティブなAUTO決定を考慮に入れた設計提案

---

## Claudeがコードを書く際のガイドライン

### Interpreter関連のコード

```python
# 推奨されるパターン
from gui_agent_loop_core.schema.core.schema import State

class InterpreterManager:
    def __init__(self):
        self.state = State.STATE_INIT

    def change_state_running(self):
        """状態をRUNNINGに変更。単調遷移を保証。"""
        if self.state != State.STATE_INIT:
            raise InvalidStateTransitionError(
                f"Cannot transition to RUNNING from {self.state}"
            )
        self.state = State.STATE_RUNNING
```

### Agent関連のコード

```python
# 推奨されるパターン
from gui_agent_loop_core.schema.core.schema import AgentName
from gui_agent_loop_core.schema.agent.schema import Agent

@dataclass
class Agent:
    name: AgentName  # 役割
    type: Agent  # 実装タイプ（役割とは独立）

    # AUTO:Agent.type:implementation_property を尊重
```

### Message関連のコード

```python
# 推奨されるパターン
from gui_agent_loop_core.schema.message.schema import MessageTypeEnum

# 列挙型のみ使用
message_type = MessageTypeEnum.MESSAGE  # ✅ 良い
message_type = "TEXT"  # ❌ 悪い（列挙型に含まれない）

# MAX_MESSAGE_LENGTH=100を尊重（AUTO:Message.limit:100）
MAX_MESSAGE_LENGTH = 100
if len(messages) > MAX_MESSAGE_LENGTH:
    raise MessageLimitError(f"Message history exceeds {MAX_MESSAGE_LENGTH}")
```

---

## Claudeがコードレビューをする際のチェックリスト

1. **用語の正規形**: 全ての用語が正規形で使用されているか？
2. **不変条件の違反**: hard invariantsに違反するコードがないか？
3. **状態遷移の単調性**: Stateが単調遷移しているか？
4. **AUTO決定の無視**: AUTO決定を無視した変更がないか？
5. **型安全性**: 列挙型が正しく使用されているか？

---

## Claudeとの協働

このプロジェクトでは、以下のタスクでClaudeの協力を特に歓迎します：

1. **概念の一意性の維持**: 新しい用語を導入する際のレビュー
2. **不変条件の検証**: コードがhard invariantsを遵守しているかのチェック
3. **ドキュメントの改善**: 用語の統一と明確化
4. **テストの改善**: 不変条件を検証するテストの作成

---

**最終更新**: 2026-02-04T00:00:00Z (bootstrap run v1.1 - CLAUDE.md verified - concept alignment confirmed, all 16 AUTO decisions documented, ontology v0.3, invariants v2026-02-02T05:23:14Z, ambiguities v2026-02-03T21:21:22Z - uniqueness checks passed, clarity score: 95/100)
**関連ドキュメント**:
- [AGENTS.md](AGENTS.md) - 全AI Agent向け指示
- [GLOSSARY.md](GLOSSARY.md) - 用語集
- `.concept/ontology.yml` - 概念辞書
- `.concept/invariants.yml` - 不変条件
