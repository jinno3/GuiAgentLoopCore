# GEMINI.md - Gemini向け特化指示

> プロジェクト: GuiAgentLoopCore
> 対象AIモデル: Gemini (Google)

このドキュメントは、Geminiがこのリポジトリで作業する際に従うべき特化指示を提供します。

---

## Gemini固有の推奨事項

### 1. 用語の一貫性

Geminiは、このリポジトリの`.concept/ontology.yml`で定義された正規形を優先的に使用します。

- `Interpreter` - 常に英単語の`Interpreter`を使用（日本語訳不使用）
- `Agent` - 常に英単語の`Agent`を使用（日本語訳不使用）
- `Session` - 常に英単語の`Session`を使用（日本語訳不使用）
- `Message` - 常に英単語の`Message`を使用（日本語訳不使用）

用語の完全なリストは[GLOSSARY.md](GLOSSARY.md)を参照してください。

### 2. 不変条件の遵守

Geminiは、以下のhard invariantsを絶対に違反しません：

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

Geminiは、AUTO決定（`.concept/ambiguities.yml`に記録）を暫定仕様として扱います。

- AUTO決定を変更する必要がある場合、まず`.concept/ambiguities.yml`を確認
- 変更の正当性を説明する evidence を提供
- 可能であれば、より正式な決定を提案

### 4. マルチモーダル対応

Geminiの以下の特性を活かして、このプロジェクトに貢献してください：

1. **画像理解**: アーキテクチャ図やフローチャートの理解
2. **長文コンテキスト**: `Interpreter`、`Agent`、`Session`、`Message`の複雑な相互作用の理解
3. **多言語対応**: 日本語と英語のドキュメントの一貫性維持

---

## Geminiがコードを書く際のガイドライン

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

## Geminiがコードレビューをする際のチェックリスト

1. **用語の正規形**: 全ての用語が正規形で使用されているか？
2. **不変条件の違反**: hard invariantsに違反するコードがないか？
3. **状態遷移の単調性**: Stateが単調遷移しているか？
4. **AUTO決定の無視**: AUTO決定を無視した変更がないか？
5. **型安全性**: 列挙型が正しく使用されているか？
6. **マルチモーダル整合**: 画像とテキストの説明が一致しているか？

---

## Geminiとの協働

このプロジェクトでは、以下のタスクでGeminiの協力を特に歓迎します：

1. **アーキテクチャ図の理解**: 図ベースのドキュメントの解析
2. **多言語ドキュメント**: 英語と日本語のドキュメントの一貫性維持
3. **視覚的な資料作成**: 図やチャートを用いたドキュメント作成
4. **長文コンテキストの分析**: 複雑な相互作用の詳細な分析

---

**最終更新**: 2026-02-02
**関連ドキュメント**:
- [AGENTS.md](AGENTS.md) - 全`Agent`向け指示
- [CLAUDE.md](CLAUDE.md) - Claude向け特化指示
- [GLOSSARY.md](GLOSSARY.md) - 用語集
- `.concept/ontology.yml` - 概念辞書
- `.concept/invariants.yml` - 不変条件
