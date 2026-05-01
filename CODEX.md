# CODEX.md - Codex向け特化指示

> プロジェクト: GuiAgentLoopCore
> 対象AIモデル: Codex (OpenAI)

このドキュメントは、Codexがこのリポジトリで作業する際に従うべき特化指示を提供します。

---

## Codex固有の推奨事項

### 1. 用語の一貫性

Codexは、このリポジトリの`.concept/ontology.yml`で定義された正規形を優先的に使用します。

- `Interpreter` - 常に`Interpreter`を使用
- `Agent` - 常に`Agent`を使用
- `Session` - 常に`Session`を使用
- `Message` - 常に`Message`を使用
- `State` - 常に`State`を使用
- `AutoChat` - 常に`AutoChat`を使用
- `StreamWrapper` - 常に`StreamWrapper`を使用
- `Backend` - 常に`Backend`を使用
- `Memory` - 常に`Memory`を使用（draft status）
- `Connector` - 常に`Connector`を使用
- `Converter` - 常に`Converter`を使用

用語の完全なリストは[GLOSSARY.md](GLOSSARY.md)を参照してください。

### 2. 不変条件の遵守

Codexは、以下のhard invariantsを絶対に違反しません：

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

### 3. AUTO決定の認識

Codexは、AUTO決定（`.concept/ambiguities.yml`に記録）を暫定仕様として扱います。

- AUTO決定を変更する必要がある場合、まず`.concept/ambiguities.yml`を確認
- 変更の正当性を説明する evidence を提供
- 可能であれば、より正式な決定を提案

### 4. コード生成の特性

Codexの以下の特性を活かして、このプロジェクトに貢献してください：

1. **コード補完**: 関数やクラスの実装を補完
2. **リファクタリング**: 既存のコードを整理・改善
3. **テスト生成**: 不変条件を検証するテストの作成
4. **型アノテーション**: 適切な型ヒントの追加

---

## Codexがコードを書く際のガイドライン

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
```

---

## Codexがコードレビューをする際のチェックリスト

1. **用語の正規形**: 全ての用語が正規形で使用されているか？
2. **不変条件の違反**: hard invariantsに違反するコードがないか？
3. **状態遷移の単調性**: Stateが単調遷移しているか？
4. **AUTO決定の無視**: AUTO決定を無視した変更がないか？
5. **型安全性**: 列挙型が正しく使用されているか？
6. **コードの簡潔さ**: 冗長なコードがないか？

---

## Codexとの協働

このプロジェクトでは、以下のタスクでCodexの協力を特に歓迎します：

1. **関数実装**: 未実装の関数の本体を記述
2. **テスト作成**: 不変条件を検証するテストの作成
3. **リファクタリング**: コードの整理と改善
4. **型アノテーション**: 適切な型ヒントの追加
5. **ドキュメンテーション**: ドックストリングやコメントの追加

---

## Codex特有の注意点

### コード生成時の注意

- **状態遷移**: 常に単調遷移を保証するコードを生成
- **列挙型**: 必ず列挙型の値を使用し、文字列リテラルを避ける
- **エラーハンドリング**: 適切な例外処理を含める
- **テスト**: 各不変条件に対するテストケースを生成

### リファクタリング時の注意

- **用語の一貫性**: 変数名や関数名に正規形を使用
- **不変条件の維持**: リファクタリング後も不変条件を維持
- **AUTO決定の尊重**: 暫定仕様を変更する場合は明示的にコメント

---

**最終更新**: 2026-02-02
**関連ドキュメント**:
- [AGENTS.md](AGENTS.md) - 全`Agent`向け指示
- [CLAUDE.md](CLAUDE.md) - Claude向け特化指示
- [GEMINI.md](GEMINI.md) - Gemini向け特化指示
- [GLOSSARY.md](GLOSSARY.md) - 用語集
- `.concept/ontology.yml` - 概念辞書
- `.concept/invariants.yml` - 不変条件
