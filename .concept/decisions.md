# Active AUTO Decisions (cache) — safe to delete

## AUTO:Agent.type:implementation_property
- Status: ACTIVE
- Chosen: AgentTypeはAgentの実装タイプ別プロパティ（AgentNameの役割とは独立）
- Policy: separation_of_concerns
- Expires After Runs: 20
- Linked: AMB-AGT-001 / ASM-AGENT-002
- Revert Triggers: primary_evidence_contradiction, test_failure

## AUTO:State.lifecycle:monotonic
- Status: ACTIVE
- Chosen: 状態は単調遷移する（INIT → RUNNING → STOP）
- Policy: safety + consistency
- Expires After Runs: 20
- Linked: ASM-STATE-001 / INV-STATE-001
- Revert Triggers: primary_evidence_contradiction, test_failure

## AUTO:AutoChat.trigger:stop_only
- Status: ACTIVE
- Chosen: AutoChatはSTATE_STOP時のみ発火
- Policy: safety + user_control
- Expires After Runs: 20
- Linked: ASM-AUTO-001 / INV-AUTO-001
- Revert Triggers: primary_evidence_contradiction, security_risk

## AUTO:Memory.specs:provisional
- Status: ACTIVE
- Chosen: ウィンドウサイズk=10（rolling）、最大長100（hard limit）
- Policy: safety + reversibility
- Expires After Runs: 20
- Linked: AMB-MEM-001 / ASM-MEM-001 / INV-MEM-001
- Revert Triggers: primary_evidence_contradiction, test_failure

## AUTO:Backend.primary:gradio
- Status: ACTIVE
- Chosen: Gradioが主要バックエンド
- Policy: industry_convention
- Expires After Runs: 20
- Linked: AMB-BE-001 / ASM-BE-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:AutoChat.prompt:default_continue
- Status: ACTIVE
- Chosen: 未設定時はデフォルト継続プロンプト使用
- Policy: safety + reversibility
- Expires After Runs: 20
- Linked: AMB-AUTO-001
- Revert Triggers: primary_evidence_contradiction, security_risk

## AUTO:Message.structure:flat
- Status: ACTIVE
- Chosen: メッセージは再帰的にフラット化可能
- Policy: flexibility
- Expires After Runs: 20
- Linked: ASM-MSG-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:Agent.role:classification
- Status: ACTIVE
- Chosen: Agentはロールベースで分類される
- Policy: industry_convention
- Expires After Runs: 20
- Linked: ASM-AGENT-001 / INV-AGENT-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:Agent.role:other_default
- Status: ACTIVE
- Chosen: OTHERはデフォルト/不明のエージェント
- Policy: safety
- Expires After Runs: 20
- Linked: ASM-INV-AGENT-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:Message.limit:100
- Status: ACTIVE
- Chosen: MAX_MESSAGE_LENGTH=100はハードリミット
- Policy: safety + reversibility
- Expires After Runs: 20
- Linked: ASM-MSG-002 / INV-MESSAGE-001
- Revert Triggers: primary_evidence_contradiction, test_failure

## AUTO:State.transition:auto_on_input
- Status: ACTIVE
- Chosen: ユーザー入力時（textbox.submit）に自動的にRUNNINGに遷移
- Policy: user_experience
- Expires After Runs: 20
- Linked: ASM-STATE-002
- Revert Triggers: primary_evidence_contradiction

## AUTO:State.timer:3sec
- Status: ACTIVE
- Chosen: 状態は3秒間隔のタイマーで自動更新（t3）
- Policy: monitoring
- Expires After Runs: 20
- Linked: ASM-INV-STATE-002 / INV-STATE-002
- Revert Triggers: primary_evidence_contradiction, performance_issue

## AUTO:Backend.deployment:paths
- Status: ACTIVE
- Chosen: allowed_paths=[/tmp, /app/work, /home, /app/GuiAgentLoopCore]でセキュリティ制限
- Policy: safety + security
- Expires After Runs: 20
- Linked: ASM-BE-002 / INV-BACKEND-001
- Revert Triggers: security_risk, primary_evidence_contradiction

## AUTO:Session.jwt:algorithm_hs256
- Status: ACTIVE
- Chosen: JWTはHS256アルゴリズム使用（暫定）
- Policy: safety + industry_convention
- Expires After Runs: 20
- Linked: ASM-SESSION-001 / INV-SESSION-002
- Revert Triggers: primary_evidence_contradiction, security_risk

## AUTO:Message.roles:tool_function_separation
- Status: ACTIVE
- Chosen: TOOLとFUNCTIONは異なるセマンティクスを持つ（暫定）
- Policy: safety + flexibility
- Expires After Runs: 20
- Linked: ASM-MSG-003 / AMB-MSG-001
- Revert Triggers: primary_evidence_contradiction, framework_integration_issue

## AUTO:Memory.implementation:dual_provisional
- Status: ACTIVE
- Chosen: 両者は暫定的に共存（移行期間中とみなす）
- Policy: reversibility + caution
- Expires After Runs: 20
- Linked: AMB-MEM-002
- Revert Triggers: primary_evidence_contradiction, performance_issue, maintenance_burden

## AUTO:Security.secret_key:env_var_required
- Status: ACTIVE
- Chosen: ハードコードされたシークレットキーはセキュリティリスク（環境変数使用へ移行必須）
- Policy: security_first
- Expires After Runs: 10
- Linked: AMB-SEC-001
- Revert Triggers: primary_evidence_contradiction, security_risk_escalation

## AUTO:Backend.timer:3sec_interval
- Status: ACTIVE
- Chosen: 3秒タイマーは妥当な更新頻度（暫定）
- Policy: monitoring + user_experience
- Expires After Runs: 20
- Linked: ASM-INV-BACKEND-002 / INV-BACKEND-002
- Revert Triggers: primary_evidence_contradiction, performance_issue

## AUTO:Connector.layer:domain
- Status: ACTIVE
- Chosen: Connectorは正規概念（domain層）
- Policy: architectural_pattern
- Expires After Runs: 20
- Linked: AMB-CON-001
- Revert Triggers: primary_evidence_contradiction, architectural_clarification
