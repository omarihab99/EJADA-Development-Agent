# GitHub Copilot Model Policy - Development Agent Suite

> **Version 1.1 · Last reviewed 2026-08-24 · Owner: ECC AI CoE**
>
> Re-verify supported models, retirement status, organization availability, and approval requirements monthly and before release.

## 1. Decision principle

## 1. Purpose

This policy defines model validation and resolution for custom agents.

It distinguishes:

- **Declared Model**: `model:` in the target agent frontmatter
- **Model Status**: supported, retiring, retired, utility-only, malformed, unavailable, blocked, approval-gated, or not declared
- **Resolved Model**: configured model retained or policy result recommended after validation
- **Parent Session Model**: model displayed for the Universal Orchestrator session
- **Observed Runtime Model**: actual specialist execution model only when platform telemetry explicitly exposes it

The parent session model is not proof of the delegated specialist runtime model.

---

## 2. Resolution order

Apply in this order:

1. **Valid supported pin**
   - Preserve the target agent's declared model.
   - Report `Resolution: Keep declared pin`.

2. **Retiring but currently supported pin**
   - Preserve it for the current execution if organization policy allows it.
   - Report the retirement risk and recommend migration.

3. **Retired, utility-only, malformed, unavailable, or blocked pin**
   - Do not treat the invalid pin as executable.
   - Resolve from the task-class defaults.
   - Disclose the original pin, status, replacement, and reason.

4. **No pin**
   - Resolve from the task-class defaults.
   - Recommend adding a reviewed pin for reproducibility.

5. **Approval-gated model**
   - Stop and request the named approval.
   - Do not silently fall back unless policy explicitly permits it.

6. **Resolved default unavailable**
   - Use the fallback in the same task class.
   - If unavailable, use `Auto` and disclose the fallback.

---

## 3. Task-class defaults

Task-class defaults are fallbacks for missing or invalid pins. They do not silently replace a valid supported pin.

| Task class | Default | Fallback | Rationale |
|---|---|---|---|
| Orchestration and routine multi-agent planning | `Claude Sonnet 5` | `Claude Opus 5` | Balanced quality, latency, and cost |
| Critical arbitration or high-consequence architecture | `Claude Opus 5` | `Claude Opus 4.8` | Premium reasoning for high-impact decisions |
| Day-to-day coding, refactor, and review | `Claude Sonnet 5` | `GPT-5.4` | Strong quality-per-cost |
| Autonomous multi-file implementation | `GPT-5.3-Codex` | `Claude Sonnet 5` | Long implementation runs |
| Large-codebase survey or migration analysis | `Claude Opus 5` | `GPT-5.6 Terra` | Extended-context requirement |
| Tests and QA | `GPT-5 mini` | `Claude Haiku 4.5` | High-volume, lower-judgment work |
| Documentation, changelogs, and boilerplate | `GPT-5 mini` | `Claude Haiku 4.5` | Cost-efficient structured generation |
| Fast interactive Q&A and terminal help | `Claude Haiku 4.5` | `GPT-5.4 mini` | Latency first |
| Unclassifiable or mixed | `Auto` | N/A | Platform selection with disclosure |

Premium escalation requires at least one documented reason:

- High consequence of error
- Deep multi-step reasoning
- Conflicting cross-domain constraints
- Regulated security or architecture decision
- Extended context requirement
- Observed lower-cost-model failure
- Explicit user request after cost disclosure

## 4. Decision categories

## 4. Cost optimization

Cost optimization is a recommendation layer, not permission to silently override a valid supported agent pin.

For each decision report:

- Declared Model
- Model Status
- Resolved Model
- Resolution Reason
- Lower-cost recommendation, if applicable
- Upgrade condition, if applicable
- Runtime Verification

If a valid pin is unnecessarily expensive for the agent's stable workload, recommend a reviewed frontmatter change for future executions.

---

## 5. Runtime verification

Valid runtime evidence must come from a platform-controlled event, log, footer, or telemetry API that explicitly identifies the model for that specialist invocation.

The following are not proof:

- Parent model picker
- Parent response footer
- Agent self-report
- Hardcoded `DECLARED_MODEL=` text
- Writing-style differences
- Orchestrator inference

When telemetry is unavailable, write:

`Runtime verification: Not exposed by runSubagent telemetry.`

Do not state that the runtime ignored or used a pin without evidence.

---

## 6. Model status reference

The exact model list and dates must be verified against the official supported-model source before publication or automated remediation.

Maintain these categories in the audit script and this policy together:

- Supported and approved
- Approval-gated
- Retiring
- Retired
- Utility-only
- Organization-blocked
- Unavailable

Do not preserve stale counts or dates as permanent policy text. Store current audit counts in `registry/MODEL_AUDIT.md`.

### Known remediation mappings from the current suite audit

| Invalid or legacy pin | Resolution guidance |
|---|---|
| `GPT-4.1` | Resolve by task class |
| `GPT-5` | Resolve by task class |
| `Claude Sonnet 4` | `Claude Sonnet 5` or task-class default |
| `Claude Sonnet 4.5` / `4.6` | Migrate to `Claude Sonnet 5` before retirement |
| `GPT-5.1-Codex` family | `GPT-5.3-Codex` |
| `GPT-4o` / `GPT-4o mini` when utility-only | Resolve by task class |
| Malformed YAML value | Replace with one supported scalar string |
| Missing pin | Task-class default, then reviewed frontmatter update |

Revalidate mappings before applying them.

---

## 7. YAML validity

Valid:

```yaml
model: Claude Sonnet 5
```

Valid:

```yaml
model: "Claude Sonnet 5"
```

Invalid:

```yaml
model:
  - Claude Sonnet 5
```

Invalid:

```yaml
model: Claude Sonnet 5 | GPT-5.4
```

The value must be one scalar string containing one model name.

---

## 8. Audit and remediation

Report only:

```bash
python scripts/model_audit.py --report
```

Propose fixes:

```bash
python scripts/model_audit.py --fix
```

`--fix` must not commit, push, merge, or bypass review.

Recommended sequence:

1. Malformed values
2. Retired pins
3. Imminently retiring pins
4. Utility-only or blocked pins
5. High-traffic unpinned agents
6. Remaining unpinned agents in reviewed batches

Record changes in the registry with old model, status, task class, new model, reason, reviewer, and date.

---

## 9. Verification tests

Validate at least:

1. Valid pinned agent retains the pin.
2. Retired pin resolves by task class and discloses substitution.
3. Unpinned coding agent resolves to coding default.
4. Unpinned architecture agent resolves to architecture default.
5. Approval-gated model stops for approval.
6. Parent `Auto` mode is not reported as specialist runtime evidence.
7. Runtime telemetry limitation is explicitly reported.
