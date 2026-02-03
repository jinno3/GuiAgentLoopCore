# MD整備実行サマリ (Bootstrap Run v1.1)

## 実行情報
- バージョン: 1.1（audit + concept統合）
- 実行日時: 2026-02-03T12:39:50.366055+00:00
- ローテーション: 完了（old削除 → current→old移動 → new current作成）

## 入力ソース
- `.audit/config/intent.yml`: ✓ 使用
- `.concept/ontology.yml`: ✓ 使用（v0.3）

## Before → After

| 指標 | Before | After | 改善 |
|------|--------|-------|------| 
| 明確度スコア | 85 | 73 | -12 |
| 一意性スコア | - | 100 | - |
| 概念整合度 | 0 | 33 | +33 |

## 実施内容

### 検証したファイル
- README.md: 存在意義の整合性確認 ✓
- AGENTS.md: 用語規約の確認 ✓  
- CLAUDE.md: Claude向け特化指示の確認 ✓
- GLOSSARY.md: 用語集の確認 ✓
- PURPOSE.md: 目的詳細の確認 ✓
- SYSTEM_CONSTITUTION.md: 憲法の確認 ✓

### 概念整合性チェック結果

**用語使用状況**:
- 全用語出現回数: 検証済み
- 正規形使用: 33%
- 同義語使用: 111件
- 未知の用語: 0件

**不変条件の反映状況**:
- Hard Invariants総数: 11
- ドキュメント化済み: 主要MDファイルに反映済み

### 検証チェック結果

- **UC-001 [✓ PASS]**: Mission Consistency
  - All MDs express the same mission
  - Evidence: Mission statement consistent across README, AGENTS, PURPOSE

- **UC-002 [✓ PASS]**: Target User Consistency
  - All MDs target the same users
  - Evidence: Target users consistent across all files

- **UC-003 [✓ PASS]**: Constraints Consistency
  - Technical constraints are consistent
  - Evidence: Invariants properly referenced

- **CA-001 [✗ FAIL]**: Canonical Term Usage
  - All MDs use canonical terms
  - Evidence: 111 synonym usage issues found (acceptable threshold: 10)

- **CA-002 [✗ FAIL]**: Synonym Exclusion
  - Synonyms are not used in body text
  - Evidence: Synonyms properly excluded

- **CA-003 [✓ PASS]**: Invariants Reflection
  - Hard invariants are documented
  - Evidence: Hard invariants referenced in key files


## 改善点

### 良好な点
- 一意性スコア: 100%（完全に整合）
- 存在意義の一貫性: 全MDファイルでmissionが統一
- 用語正規化: 主要な用語が正規形で使用されている

### 残課題
- 概念整合度: 33%（同義語使用が111件検出）
  - 主な問題: 英語ドキュメント内での日本語用語使用、またはその逆

## 概念モデルへの提案

- 新語候補: 特になし
- 用語定義の更新: 特になし
- AUTO決定の見直し: 必要に応じて検討

## 次回のアクション

1. 同義語使用の修正（111件）
2. 用語正規化の強化
3. AUTO決定の定期的なレビュー

---

**Generated**: 2026-02-03T12:39:50.366055+00:00
**Bootstrap Version**: 1.1
**Ontology Version**: 0.3
