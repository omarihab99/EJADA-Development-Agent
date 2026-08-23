# Model Policy Audit

**Generated:** 2026-08-19  
**Scope:** Development agent suite  
**Status:** Baseline counts below are inherited from the 2026-08-17 audit supplied for this update. Re-run the audit before treating counts or model status as current.

## Baseline summary

| Status | Count | Required response |
|---|---:|---|
| Retired | 56 | Replace by task class; disclose substitutions until remediated |
| Sunset | 17 | Prioritize migration before the recorded retirement date |
| Utility-only | 2 | Replace; never pin picker-ineligible utility models |
| Malformed | 4 | Normalize to one valid scalar |
| Unpinned | 142 | Assign by task class and traffic priority |
| Valid at baseline | 4 | Re-verify live support status |

## Mandatory audit checks

1. Parse each agent's frontmatter and preserve raw declared value.
2. Validate that `model:` is one scalar.
3. Compare normalized value with live-supported, sunset, retired, blocked, and utility-only sets.
4. Classify the agent using evidence from purpose, workflow, tools, and delegation.
5. Propose default and fallback from `MODEL_POLICY.md`.
6. Flag premium selections without exception evidence.
7. Flag orchestrators using low-capability models and simple agents using premium models.
8. Record verification date and source.
9. Produce a dry-run diff before writing.
10. Fail CI on new retired, malformed, blocked, utility-only, or unjustified premium pins.

## Review queue order

1. Imminent sunset pins.
2. Already retired, utility-only, and malformed pins.
3. T0 and T1 unpinned agents.
4. High-traffic T2 agents.
5. Remaining unpinned agents.

Do not remediate the entire suite in one PR. Each batch must have model tests, registry updates, rollback evidence, and approval.

## Per-agent audit record

| Agent | Path | Tier | Task class | Declared | Status | Proposed | Fallback | Rationale | Premium exception | Verified | Reviewer | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Exit criteria

- No new invalid or unsupported pins.
- All substitutions disclosed.
- Every changed agent has a task class, default, fallback, owner, and test evidence.
- Audit totals reconcile to the number of files scanned.
- Policy tables and audit status sets were verified together.
