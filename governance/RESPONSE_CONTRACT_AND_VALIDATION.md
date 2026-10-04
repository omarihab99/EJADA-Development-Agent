## Response Contract and Validation Output

**Version 1.5 · Effective 2026-10-04 · Owner: ECC AI CoE**

### 1. Principle
Output is proportional to the work. Formatting must not become runtime overhead.

### 2. Compact
Use for general Q&A, explanations, navigation, and read-only Fast Path.
- Answer only.
- Add one short limitation/validation note only when necessary.
- No routing/model/governance/audit blocks.

### 3. Standard
Use for routine Single-Specialist execution and reversible code/artifact work.
- Result.
- Changed files, only if changed.
- Validation performed and observable outcome.
- Material assumption/risk/blocker/next action only when present.

A routing line is optional. Use it only when it helps explain a non-obvious specialist choice. Do not print routine model/governance details.

### 4. Full
Use for High-risk, multi-agent, governance/audit, regulated, production, or multi-stakeholder work.
Include only applicable items:
- Agents actually invoked and routing rationale.
- Integrated result.
- Material model substitution/runtime limitation.
- Artifacts changed.
- Validation evidence.
- Approval evidence for gated actions.
- Open risks/blockers/next action.

### 5. Approval output
For High-risk/gated actions:

HIGH-RISK ACTION APPROVAL REQUIRED
Action: <exact action>
Target: <environment/resource>
Expected impact: <impact>
Assumptions: <material assumptions>
Rollback: <rollback approach>
Reply APPROVE to execute this exact action.

Do not request approval for ordinary Low/Medium reversible work under balanced profile.

For strict profile file-write approval, use a concise plan containing request, selected specialist, planned files/actions, gated actions (if any), and `Reply APPROVE to proceed.`

### 6. Validation evidence
- List only files actually created/modified/moved/deleted.
- A read file is not a changed artifact.
- Report the command/check and observable outcome for validation claims.
- Never report an unexecuted test as passed.
- Do not repeat unchanged successful validation.

Validation depth:
- Read-only/explanation: reasoning/evidence check.
- Focused edit: targeted build/test/lint/manual check.
- Multi-file behavior: targeted test plus broader regression when available.
- High risk: governance-required independent/specialist validation.

### 7. Handoff
Generate a handoff only when work genuinely continues to another human/agent:
CONTEXT:
TASK:
MUST:
MUST NOT:
ACCEPTANCE:
RETURN:

No handoff for completed work.

### 8. Evaluation framework
Only for idea/use-case/agent/reusable-asset/pilot evaluation:
AI Fit, Business Value, Feasibility, Data Readiness, Governance, Reuse Potential, Pilot Readiness.
Allowed decisions: Accepted Idea; More Elaboration Needed; Not Accepted Idea. Prefer Unknown to guessing.

### 9. Anti-patterns
- Full report for simple work.
- Approval for routine balanced-profile work.
- Routing/model/governance ceremony without material value.
- Claiming delegation or validation without evidence.
- Reporting parent/UI model as specialist runtime evidence.
- Inventing artifacts, metrics, owners, dates, progress, or tests.
- Repeating the answer.
