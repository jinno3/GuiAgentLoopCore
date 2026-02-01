# CLAUDE.md - Claude向け特化指示

> プロジェクト: GuiAgentLoopCore
> 対象AIモデル: Claude (Anthropic)

このドキュメントは、Claudeがこのリポジトリで作業する際に従うべき特化指示を提供します。

---

## Claude固有の推奨事項

### 1. 用語の一貫性

Claudeは、このリポジトリの`.concept/ontology.yml`で定義された正規形を優先的に使用します。

- `Interpreter` - "会話インタープリタ"ではなく`Interpreter`を使用
- `Agent` - "AIエージェント"ではなく`Agent`を使用
- `Session` - "会話セッション"ではなく`Session`を使用

用語の完全なリストは[GLOSSARY.md](GLOSSARY.md)を参照してください。

### 2. 不変条件の遵守

Claudeは、以下のhard invariantsを絶対に違反しません：

```python
# 良い例: 状態遷移の単調性を尊重
def change_state_running(interpreter: Interpreter):
    if interpreter.state == InterpreterState.STATE_INIT:
        interpreter.state = InterpreterState.STATE_RUNNING
    else:
        raise InvalidStateTransitionError(
            f"Cannot transition to RUNNING from {interpreter.state}"
        )

# 悪い例: 状態の逆行
def revert_to_init(interpreter: Interpreter):  # ❌ 違反
    interpreter.state = InterpreterState.STATE_INIT
```

### 3. AUTO決定の認識

Claudeは、AUTO決定（`.concept/ambiguities.yml`に記録）を暫定仕様として扱います。

- AUTO決定を変更する必要がある場合、まず`.concept/ambiguities.yml`を確認
- 変更の正当性を説明する evidence を提供
- 可能であれば、より正式な決定を提案

### 4. ステートフルな操作の注意

Claudeは、以下のステートフルな操作で特に注意を払います：

- **State管理**: 状態遷移は常に単調的（INIT → RUNNING → STOP）
- **Session管理**: セッションIDはUUIDで一意に
- **Message処理**: メッセージタイプは列挙型のみ使用

### 5. Claude特有の強みを活かす

Claudeの以下の特性を活かして、このプロジェクトに貢献してください：

1. **長いコンテキストの理解**: `Interpreter`、`Agent`、`Session`、`Message`の複雑な相互作用を理解
2. **詳細な分析**: 不変条件違反の可能性を詳細に分析
3. **明確な説明**: 技術的な決定を明確に説明し、evidenceを提供

---

## Claudeがコードを書く際のガイドライン

### Interpreter関連のコード

```python
# 推奨されるパターン
from gui_agent_loop_core.schema.core.schema import InterpreterState

class InterpreterManager:
    def __init__(self):
        self.state = InterpreterState.STATE_INIT

    def change_state_running(self):
        """状態をRUNNINGに変更。単調遷移を保証。"""
        if self.state != InterpreterState.STATE_INIT:
            raise InvalidStateTransitionError(
                f"Cannot transition to RUNNING from {self.state}"
            )
        self.state = InterpreterState.STATE_RUNNING
```

### Agent関連のコード

```python
# 推奨されるパターン
from gui_agent_loop_core.schema.core.schema import AgentName
from gui_agent_loop_core.schema.agent.schema import AgentType

@dataclass
class Agent:
    name: AgentName  # 役割
    type: AgentType  # 実装タイプ（役割とは独立）

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

**最終更新**: 2026-02-01
**関連ドキュメント**:
- [AGENTS.md](AGENTS.md) - 全AIエージェント向け指示
- [GLOSSARY.md](GLOSSARY.md) - 用語集
- `.concept/ontology.yml` - 概念辞書
- `.concept/invariants.yml` - 不変条件
