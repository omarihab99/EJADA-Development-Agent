# GitHub Copilot Model Policy - Development Agent Suite

**Version 1.1 | Effective 2026-08-19**  
**Live support status must be re-verified before merge. The audit output, not this prose, is authoritative for suite counts.**

## 1. Decision principle

Choose the least expensive currently supported model that reliably satisfies task complexity, consequence, context, latency, and tool-use needs. A user preference is an input, not an approval. Premium selection requires positive justification.

## 2. Mandatory decision sequence

1. Identify the agent purpose and concrete tasks.
2. Rate complexity: low, standard, high, or long-horizon.
3. Rate consequence: low, medium, or high.
4. Identify context size, latency, coding autonomy, and tool-use needs.
5. Map to a task class.
6. Check live supported-model status and organization enablement.
7. Compare the proposed model with the default and fallback.
8. Challenge overpowered selections and document exceptions.
9. Record model, fallback, rationale, verification date, and approver in the registry.

## 3. Task-class policy

| Task class | Default | Fallback | Use when |
|---|---|---|---|
| Orchestration and multi-agent arbitration | `Claude Opus 5` | `GPT-5.6 Sol` | Long-horizon routing across competing constraints |
| Architecture, threat modelling, hard debugging | `Claude Opus 5` | `Claude Opus 4.8` | High-consequence reasoning with justified premium use |
| Day-to-day coding, refactor, review, agentic edits | `Claude Sonnet 5` | `GPT-5.4` | Standard engineering work |
| Autonomous multi-file implementation | `GPT-5.3-Codex` | `Claude Sonnet 5` | Long coding sessions with validated tool permissions |
| Large-codebase survey or migration analysis | `Claude Opus 5` | `GPT-5.6 Terra` | Extended context is demonstrably required |
| Tests, docs, changelogs, boilerplate, simple formatting | `GPT-5 mini` | `Claude Haiku 4.5` | High-volume, low-judgement work |
| Fast interactive Q&A and terminal guidance | `Claude Haiku 4.5` | `GPT-5.4 mini` | Latency prioritized over depth |
| Unclassifiable or mixed | `Auto` | N/A | Requirements are not yet stable |

A simple markdown formatter, spelling corrector, routine FAQ agent, or templated document generator normally maps to the low-cost class. `Claude Opus 5` is **Not recommended** unless documented high-consequence reasoning changes the task class.

## 4. Decision categories

- **Recommended:** Policy default or a cheaper option proven sufficient.
- **Acceptable with justification:** Supported alternative with explicit quality, latency, context, data, or availability justification and required approval.
- **Not recommended:** Oversized, retired, utility-only, malformed, blocked, or unsupported for the task.

## 5. Required output for model requests

```markdown
## Governance Review
**Request:** <request>
**Decision:** Approved | Conditionally Approved | Not Recommended
**Task class:** <class>
**Policy reference:** MODEL_POLICY.md section 3
**Complexity/consequence:** <assessment>
**Rationale:** <quality, cost, latency, context, and governance explanation>
**Recommended model:** <model>
**Fallback model:** <model>
**Governance requirements:** <approval, verification, tests>
**Implementation guidance:** <only after the decision>
```

## 6. Premium-model challenge

Before approving a premium model, answer all of the following:

- What requirement cannot be met by the class default?
- What evidence or test demonstrates the gap?
- Is the task high consequence, long horizon, or genuinely large context?
- What is the expected usage volume and budget impact?
- Who approves the exception and when will it be reviewed?

If these answers are missing, recommend the task-class default and mark the premium request `Not Recommended` or `Conditionally Approved` pending evidence.

## 7. Status and substitution

- A valid supported pin may be used if it matches the task class.
- Retired, sunset, utility-only, malformed, blocked, or unavailable pins must not be treated as approved.
- An absent pin requires task-class selection.
- Any substitution must be disclosed in the Response Contract.
- Update the policy status sets and audit script together after live verification.
- Never hard-code an unverified retirement claim into a governance finding. Cite the audit or live verification evidence.

## 8. Verification tests

For each model change, test representative easy, normal, and edge prompts; verify correctness, format adherence, latency, tool behavior, and failure handling. Record the selected model, fallback, date, evaluator, and result. A cheaper model wins when it passes the same acceptance criteria.
