# GitHub Copilot Model Policy - Development Agent Suite

**Version 1.2 · Last reviewed 2026-09-09 · Owner: ECC AI CoE**

## 1. Loading policy

Do not load this file during Fast Path execution.
Consult it only when:
- A specialist will be delegated.
- A model pin is missing, invalid, unavailable, blocked, or approval-gated.
- The user requests model selection, audit, or remediation.
- A release or maintenance task requires model verification.

Cache the resolved model decision for the current execution. Reload only if the target agent, organization availability, or policy changes.

## 2. Definitions

- **Declared Model:** `model:` in the target agent frontmatter.
- **Model Status:** supported, retiring, retired, utility-only, malformed, unavailable, blocked, approval-gated, or not declared.
- **Resolved Model:** retained valid pin or task-class fallback.
- **Parent Session Model:** model used by the Universal Orchestrator.
- **Observed Runtime Model:** specialist model only when platform telemetry explicitly exposes it.

The parent session model and an agent self-report are not proof of the specialist runtime model.

## 3. Resolution order

1. Preserve a valid, supported, organization-allowed declared pin.
2. Preserve a retiring but still supported pin for the current execution, and recommend migration.
3. For retired, utility-only, malformed, unavailable, or blocked pins, use the task-class default.
4. For no pin, use the task-class default and recommend reviewed pinning for high-traffic agents.
5. For approval-gated models, request approval only when that model is genuinely required. Otherwise use an allowed fallback and disclose it.
6. If the default is unavailable, use the fallback, then Auto.

Do not silently replace a valid pin only to reduce cost.

## 4. Task-class defaults

| Task class | Default | Fallback |
|---|---|---|
| Fast interactive Q&A and terminal help | Claude Haiku 4.5 | GPT-5.4 mini |
| Documentation, changelog, boilerplate | GPT-5 mini | Claude Haiku 4.5 |
| Tests and routine QA | GPT-5 mini | Claude Haiku 4.5 |
| Day-to-day coding, refactor, review | Claude Sonnet 5 | GPT-5.4 |
| Routine orchestration and multi-agent planning | Claude Sonnet 5 | GPT-5.4 |
| Autonomous multi-file implementation | GPT-5.3-Codex | Claude Sonnet 5 |
| Critical arbitration or high-consequence architecture | Claude Opus 5 | Claude Sonnet 5 |
| Large-codebase survey requiring extended context | Approved extended-context model | Auto |
| Unclassifiable or mixed | Auto | N/A |

Use standard context and normal reasoning by default. Increase context or reasoning only when the task requires it.

## 5. Premium escalation

Premium escalation requires at least one recorded reason:
- High consequence of error.
- Conflicting cross-domain constraints.
- Regulated security or architecture decision.
- Extended-context requirement.
- Observed lower-cost-model failure.
- Explicit user request after cost disclosure.

Routine repository routing is not, by itself, a reason for premium escalation.

## 6. Runtime reporting

For routine execution, report model details only when a substitution, limitation, approval, or material cost decision occurred.

For Full reporting, include:
- Declared Model.
- Model Status.
- Resolved Model.
- Resolution Reason.
- Runtime Verification.

When telemetry is unavailable, write:

`Runtime verification: Not exposed by runSubagent telemetry.`

## 7. Audit and remediation

Model lists and retirement dates change. Verify against the official supported-model source before publication or automated remediation.

Commands:

```bash
python scripts/model_audit.py --report
python scripts/model_audit.py --fix
```

`--fix` must produce reviewable changes and must not commit, push, merge, or bypass review.

Remediation sequence:
1. Malformed values.
2. Retired and utility-only pins.
3. Imminently retiring pins.
4. High-traffic unpinned T0/T1/T2 agents.
5. Remaining unpinned agents in reviewed batches.

## 8. Required tests

Validate that:
- Fast Path does not load model policy.
- Valid pins are preserved.
- Invalid and missing pins resolve by task class.
- Parent model is not reported as specialist runtime evidence.
- Approval-gated model handling follows organization policy.
- Unavailable defaults use the documented fallback.
