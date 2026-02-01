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
