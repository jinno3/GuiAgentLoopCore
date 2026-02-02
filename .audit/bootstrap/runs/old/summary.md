# MD整備実行サマリ

## 実行情報
- バージョン: 1.1（audit + concept統合）
- 実行日時: 2026-02-02T04:01:32.053366+00:00
- ローテーション: old削除 → current→old移動 → new current作成

## 入力ソース
- `.audit/config/intent.yml`: ✓ 使用
- `.concept/ontology.yml`: ✓ 使用（11用語、うちcore 5）

## Before → After

| 指標 | Before | After | 改善 |
|------|--------|-------|------|
| 明確度スコア | 79 | 79 | +0 |
| 一意性スコア | - | 100 | - |
| **概念整合度** | 79 | 79 | +0 |
| 全体スコア | - | 80 | - |

## 用語正規化の状況

### 用語統計
- 総canonical terms: 11
- Core terms: 5
- Domain terms: 5
- Aux terms: 1

### 同義語マッピング
- 総同義語数: 31

### 概念整合チェック結果
- **一意性スコア**: 100 (2/2)
- **概念整合スコア**: 50
- **全体スコア**: 80

### 用語使用状況
- Canonical使用回数: 231
- 同義語使用回数: 116
- 整合率: 66.6%

## 実施内容

### 確認したファイル
- README.md: 存在意義の整合性確認 ✓
- AGENTS.md: AIエージェント向け指示の整合性確認 ✓
- CLAUDE.md: Claude向け特化指示の整合性確認 ✓
- GLOSSARY.md: 概念辞書との同期確認 ✓
- PURPOSE.md: 目的の整合性確認 ✓
- SYSTEM_CONSTITUTION.md: 不変条件の反映確認 ✓

### 検証チェック結果
- [✓] UC-001: Mission Consistency - Mission statement consistent across MDs
- [✓] UC-005: Intent.yml Alignment - MD files align with intent.yml
- [✗] CA-001: Canonical Term Usage - Found 116 synonym usages vs 231 canonical usages
- [✗] CA-002: Synonym Exclusion - 116 synonym usages found in documentation
- [✓] CA-003: Hard Invariant Reflection - 11 hard invariants defined in ontology
- [✓] CA-004: AUTO Decision Documentation - 8 AUTO decisions documented in ambiguities.yml

## 不変条件の反映状況
- 総invariants: 14
- Hard invariants: 11
- MDに反映済み: 11

## AUTO決定の扱い
- アクティブなAUTO決定: 8
- ドキュメント化済み: 8

## 残課題
- 同義語使用が116箇所見つかりました（説明目的での使用を含む）
- 概念整合スコアを90%以上に向上させる余地あり

## 概念モデルとの連携
- オントロジーが正常にロードされました
- 用語の正規形が一貫して使用されています
- AUTO決定がambiguities.ymlで追跡されています

## 今後の改善提案
1. 同義語使用を最小限に抑える（説明目的以外ではcanonical formを使用）
2. GLOSSARY.mdの拡張（すべてのcanonical termsを網羅）
3. 新規用語の登録プロセスの強化
---

**生成ツール**: 16_repo_md_bootstrapper v1.1  
**検証日時**: 2026-02-02T04:01:32.053445+00:00
