## GitHub Copilot Model Policy - Development Agent Suite

**Version 1.5 · Last reviewed 2026-10-04 · Owner: ECC AI CoE**

### 1. Lazy loading
Do not load this policy for Fast Path. Do not load it merely because a specialist is delegated when the specialist already has a valid, supported, allowed pin and no model analysis is requested.

Consult it only when:
- selected specialist has no valid supported allowed pin;
- the pin is retiring/retired/utility-only/malformed/unavailable/blocked/approval-gated;
- validation justifies escalation;
- user requests model selection/audit/remediation;
- release/maintenance requires verification.

Cache the decision for the current execution; reload only when agent, availability, or policy changes.

### 2. Runtime truth
- Declared Model: target agent frontmatter `model:`.
- Resolved Model: retained valid pin or policy fallback.
- Parent Session Model: orchestrator model.
- Observed Runtime Model: only telemetry explicitly exposed by the platform.

Parent/UI selection and agent self-report are not proof of specialist runtime model. Static body text does not change runtime model selection.

### 3. Resolution order
1. Preserve valid supported organization-allowed declared pin.
2. For retiring-but-supported pin, preserve for current execution and flag maintenance separately, not in routine user output unless relevant.
3. For invalid/unavailable/retired/utility-only/blocked/no pin, choose task-class default.
4. If default unavailable, choose fallback, then Auto.
5. Approval-gated model: use an allowed qualified fallback unless the gated model is genuinely required.
6. Validation failure: refine once when safely correctable, otherwise escalate to next qualified model.

Do not replace a valid pin solely for cost. Do not use premium models for routine routing.

### 4. Task-class defaults
- Fast interactive Q&A / terminal help: Claude Haiku 4.5; fallback GPT-5.4 mini.
- Documentation / changelog / boilerplate: GPT-5 mini; fallback Claude Haiku 4.5.
- Tests / routine QA: GPT-5 mini; fallback Claude Haiku 4.5.
- Day-to-day coding / refactor / review: Claude Sonnet 5; fallback GPT-5.4.
- Routine orchestration / multi-agent planning: Claude Sonnet 5; fallback GPT-5.4.
- Autonomous multi-file implementation: GPT-5.3-Codex; fallback Claude Sonnet 5.
- Critical arbitration / high-consequence architecture: Claude Opus 5; fallback Claude Sonnet 5.
- Large-codebase survey requiring extended context: approved extended-context model; fallback Auto.
- Unclassifiable/mixed: Auto.

Use standard context/reasoning by default; increase only when task evidence requires it.

### 5. Benchmark use
Read `MODEL_BENCHMARKS.csv` only when a model decision benefits from benchmark evidence. A benchmark governs selection only when it identifies a matching agent or benchmark key and task class. Rows without that match are informational.

Qualification:
- Remove ineligible models.
- Enforce required quality first.
- Prefer lowest expected credits among qualified models.
- If cost evidence is equal/unavailable, prefer fewer expected tokens.
- Next tie-breaker is measured accuracy.
- If no benchmark qualifies, use task-class default and validate.

Premium escalation requires at least one: high consequence of error; conflicting cross-domain constraints; regulated security/architecture; extended context; observed cheaper-model failure; explicit user request after material cost disclosure.

### 6. Reporting
Routine execution: do not report model details unless substitution, limitation, approval, or material cost decision occurred.
Full reporting: include declared/status/resolved/reason/runtime verification when relevant.
If telemetry is unavailable: `Runtime verification: not exposed by runSubagent telemetry.`

### 7. Audit/remediation
Supported models and retirement status are time-sensitive. Verify the official supported-model source before publication or automated remediation.

Repository commands when present:
`python scripts/model_audit.py --report`
`python scripts/model_audit.py --fix`

`--fix` must produce reviewable changes and must not commit/push/merge/bypass review.
Prioritize malformed/retired/utility-only, then imminent retirement, high-traffic unpinned T0/T1/T2, then remaining unpinned agents.

### 8. Required policy tests
- Fast Path does not load model policy.
- Valid pins avoid unnecessary policy/benchmark loading.
- Invalid/missing pins resolve by task class.
- Agent selection precedes model selection.
- Parent model is never runtime evidence.
- Unavailable default falls back as documented.
- Benchmark evidence cannot bypass quality threshold.
- Premium escalation requires a recorded reason.
- Validation failure causes controlled refinement/escalation.
