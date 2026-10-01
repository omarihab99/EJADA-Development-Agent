# Response Contract and Validation Output

**Version 1.3 · Effective 2026-10-01 · Owner: ECC AI CoE**

## 1. Purpose

This document defines proportionate response formats. It does not select agents or models.

## 2. Response tiers

### Compact
Use for general Q&A, explanations, navigation, and read-only Fast Path work.

Output:
- The answer only.
- Add a short limitation or validation note only when necessary.

Do not include routing, model, runtime, cost, approval, artifact, handoff, or tracker sections.

### Standard
Use for routine code or artifact changes and single-specialist execution.

Output:
1. Result.
2. Changed files.
3. Validation performed and outcome.
4. Remaining assumptions, risks, or next action only when applicable.

Do not add empty `N/A` sections.

### Full
Use for multi-agent, governance, regulated, production, high-risk, or multi-stakeholder work.

Output:
1. Routing and agents actually invoked.
2. Integrated result.
3. Model substitutions or runtime limitations, when relevant.
4. Artifacts changed.
5. Validation evidence.
6. Approval evidence for high-risk actions.
7. Open risks, blockers, and next actions.

## 3. Routing output

For routine single-specialist execution, emit one concise line before execution:

`🤖 Agent: <exact verified agent name> | Reason: <one short clause>`

Use the detailed routing block only for Full-tier execution:

```text
Routing Decision
- Proposed Agent:
- Task:
- Routing Reason:
- Execution Wave:
- Model Decision, only when material:
- Governance Status:
```

Never claim an agent was invoked unless the corresponding tool call occurred.

## 4. Approval output

Do not emit approval output before ordinary specialist delegation or reversible local changes.

For a high-risk action, emit:

```text
HIGH-RISK ACTION APPROVAL REQUIRED
Execution has stopped before the risky action.
Action:
Target environment or resource:
Expected impact:
Assumptions:
Rollback approach:
Type APPROVE to execute this exact action, MODIFY to revise it, or REJECT to cancel it.
```

Approval applies only to the exact named action. A plan approval does not authorize another irreversible action.

## 5. Artifact and validation reporting

List only files created, modified, moved, or deleted. Files merely read are not artifacts.

Validation claims must include the command or check performed and its observable outcome. Never report a test as passed if it was not executed.

## 6. Handoff prompt

Include a handoff only when work genuinely continues with another person or agent:

```text
CONTEXT:
TASK:
MUST:
MUST NOT:
ACCEPTANCE:
RETURN FORMAT:
```

Do not generate a handoff for a completed task.

## 7. Validation framework

Use only when evaluating an idea, use case, agent, reusable asset, or pilot.

Dimensions:
- AI Fit.
- Business Value.
- Feasibility.
- Data Readiness.
- Governance.
- Reuse Potential.
- Pilot Readiness.

Allowed decisions:
- Accepted Idea.
- More Elaboration Needed.
- Not Accepted Idea.

Unknown is preferred over guessing.

## 8. Anti-patterns

- Full reporting for a simple question.
- Approval before routine delegation.
- Claiming delegation before execution.
- Reporting the parent model as specialist runtime evidence.
- Inventing files, owners, dates, metrics, tests, or progress.
- Repeating the answer across multiple sections.
- Listing files that were only read as changed artifacts.
