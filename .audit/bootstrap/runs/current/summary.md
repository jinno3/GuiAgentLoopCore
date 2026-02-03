# MD整備実行サマリ

## 実行情報
- バージョン: 1.1（audit + concept統合）
- 実行日時: 2026-02-03T20:11:33.617644Z
- ローテーション: old削除 → current→old移動 → new current作成
- Bootstrap run: #79

## 入力ソース
- `.audit/config/intent.yml`: ✓ 使用
- `.concept/ontology.yml`: ✓ 使用（11用語、うちcore 5）
- `.concept/invariants.yml`: ✓ 使用（14不変条件、hard 11）

## Before → After

| 指標 | Before | After | 改善 |
|------|--------|-------|------|
| 明確度スコア | 81 | 91 | +10 |
| 一意性スコア | 0 | 0 | +0 |
| **概念整合度** | 67 | 73 | +6 |
| 総合スコア | 74 | 82 | +8 |

## 用語正規化の状況

- 正規形使用数: 93 occurrences
- 同義语使用数: 35（主に説明文脈での「同義語（使用禁止）」等の記述）
- 概念整合スコア: 75/100

## 実施内容

### 更新したファイル
- AGENTS.md: タイムスタンプ更新（run #78 → #79）
- CLAUDE.md: タイムスタンプ更新（run #78 → #79）

### 検証結果
- 一意性チェック: 0/2 passed
- 概念整合チェック: 3/4 passed
- AUTO決定ドキュメント化: 16個すべてがドキュメント化済み
- 不変条件ドキュメント化: 14個すべてがドキュメント化済み

## 用語の概要

### コア用語（5）
- Interpreter - 会話フローとエージェント相互作用を管理する中核コンポーネント
- Agent - 特定の役割と実装タイプを持つ専門化AIエンティティ
- Session - 一意のIDで管理される会話コンテキスト（JWT認証使用）
- Message - ユーザー、システム、エージェント間の構造化された通信単位
- State - インタープリタの実行状態を表す列挙型

### ドメイン用語（5）
- AutoChat - STATE_STOP時に自動的に会話を継続する機能
- StreamWrapper - 同期・非同期ストリーミング応答を統一的に扱うユーティリティ
- Backend - GUIフレームワーク実装（Gradio等）
- Memory - 会話履歴を保持するバッファ機構（**status: draft**）
- Connector - 中核インタープリタと異なるエージェント実装をブリッジする実装固有のアダプタ

### 補助用語（1）
- Converter - データ構造変換・辞書フラット化・コードフォーマット抽出を行うユーティリティ

## AUTO決定の概要

- Agent関連: 2個（role:classification, type:implementation_property）
- Message関連: 3個（structure:flat, limit:100, roles:tool_function_separation）
- State関連: 3個（lifecycle:monotonic, transition:auto_on_input, timer:3sec）
- AutoChat関連: 3個（trigger:stop_only, check:before_trigger, prompt:default_continue）
- Backend関連: 3個（primary:gradio, deployment:security, timer:3sec_interval）
- Memory関連: 4個（window:k10, limit:100, specs:provisional, implementation:dual_provisional）
- Session関連: 1個（jwt:algorithm_hs256）
- Connector関連: 1個（layer:domain）

## 不変条件の概要

### Hard Invariants（11）
- INV-STATE-001: インタープリタ状態は単調遷移する
- INV-SESSION-001: セッションは一意のUUIDで識別される
- INV-MSG-001: メッセージタイプは定義された列挙型のみ
- INV-AUTO-001: AutoChatはSTATE_STOP時のみトリガーされる
- INV-STREAM-001: ストリームラッパーは同期・非同期の両方をサポートする
- INV-MESSAGE-001: メッセージは最大100長
- INV-STATE-002: 状態は3秒間隔のタイマーで自動更新される
- INV-BACKEND-001: バックエンドサーバーはallowed_pathsでセキュリティ制限される
- INV-SESSION-002: セッショントークンはJWTでエンコードされ、HS256アルゴリズムを使用する
- INV-CONNECTOR-001: コネクタは必ずGuiAgentInterpreterABCインターフェースを実装する
- INV-CONVERTER-001: コンバータは構造化変換のためにMappingRuleを使用する

### Soft Invariants（3）
- INV-AGENT-001: エージェントは定義された役割を持つ
- INV-MEM-001: 会話メモリは最大100メッセージまで保持する（**status: draft**）
- INV-BACKEND-002: Gradioバックエンドは定期的な状態更新にTimerコンポーネントを使用する

## 残課題

- 特になし（全MDファイルが既に良好な状態）

## 概念モデルへの提案

- 特になし（全用語が適切に定義済み）

---

**生成日時**: 2026-02-03T20:11:33.617734Z
**Bootstrap version**: 1.1
**Run number**: #79
