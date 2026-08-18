# GitHub Copilot Model Policy — Development Agent Suite

**Version 1.0 · Verified 2026-08-17 against `docs.github.com` → Copilot → Reference → AI models → Supported models**
**Re-verify monthly. Model availability and retirement dates change without notice.**

---

## 1. Why this policy exists

An agent's `model:` frontmatter is optional. When absent, the model is whatever the user happens to
have selected in their picker — so the same agent produces different quality, cost, and latency for
different people, and results are not reproducible.

**Current suite state (audited 2026-08-17, 225 files):**

| Status | Count | Meaning |
|---|---:|---|
| No `model:` declared | 142 | Behaviour depends on the user's picker |
| Pins a **retired** model | 56 | Pin is dead; Copilot falls back silently |
| Pins a model **retiring 2026-09-01** | 17 | Breaks in 15 days |
| Pins a **utility-only** model | 2 | Not selectable in the picker |
| Malformed value | 4 | List literal / YAML list item / pipe-delimited string |
| Currently valid | 4 | — |

**Only 4 of 225 agents carry a valid, current model pin** — `azure-smart-city-iot-architect`,
`azure-verified-modules-owner-triage`, `cloud-saas-outage-triage`, and `ember`.
Counts are produced by `scripts/model_audit.py`; that tool is authoritative over this table.

---

## 2. Selection rules

Resolution order for the orchestrator and for any agent author:

1. Agent declares a **currently supported** model → use it.
2. Agent declares a **retired, utility-only, or malformed** model → ignore the pin, select by task
   class (Section 3), and **disclose the substitution** in the response.
3. Agent declares **nothing** → select by task class.
4. Org policy blocks the selection → next row in the same task class → then `Auto`.

---

## 3. Task-class defaults

| Task class | Default | Fallback | Rationale |
|---|---|---|---|
| Orchestration, multi-agent planning, arbitration | `Claude Opus 5` | `GPT-5.6 Sol` | Long-horizon reasoning over many simultaneous constraints |
| Architecture, ADRs, threat modelling, hard debugging | `Claude Opus 5` | `Claude Opus 4.8` | High consequence, low volume — justify the premium |
| Day-to-day coding, refactor, review, agentic edits | `Claude Sonnet 5` | `GPT-5.4` | Best quality-per-credit for the bulk of the work |
| Autonomous multi-file implementation runs | `GPT-5.3-Codex` | `Claude Sonnet 5` | Purpose-built for long coding sessions |
| Large-codebase survey / migration analysis | `Claude Opus 5` (1M context) | `GPT-5.6 Terra` | Extended context is a requirement, not a preference |
| Tests, docs, changelogs, boilerplate | `GPT-5 mini` | `Claude Haiku 4.5` | High volume, low judgement — protect the budget |
| Fast interactive Q&A, terminal help | `Claude Haiku 4.5` | `GPT-5.4 mini` | Latency over depth |
| Unclassifiable / mixed | `Auto` | — | Note the choice in the report |

**Extended capability guidance:** the 1M-token context window and configurable reasoning levels both
increase credit consumption. Use standard context and standard reasoning by default; escalate only
for genuinely large or genuinely hard tasks, and say why.

---

## 4. Model status reference (as verified 2026-08-17)

### Currently GA and safe to pin

`Claude Opus 5` · `Claude Sonnet 5` · `Claude Opus 4.7` · `Claude Opus 4.8` · `Claude Haiku 4.5` ·
`GPT-5.5` · `GPT-5.6 Luna` · `GPT-5.6 Sol` · `GPT-5.6 Terra` · `GPT-5.4` · `GPT-5.4 mini` ·
`GPT-5 mini` · `GPT-5.3-Codex` · `Gemini 3.5 Flash` · `Gemini 3.6 Flash` · `Gemini 3.7 Flash` ·
`MAI-Code-1-Flash` · `MAI-Code-1.1-Flash` · `Grok 4.5` · `Grok 4.6`

### Approval-gated

| Model | Constraint |
|---|---|
| `Claude Fable 5` | Distinct data-retention posture; not eligible for default enablement; enterprise must explicitly enable |
| `Kimi K2.7 Code`, `Kimi K3` | Open weight; not eligible for default enablement |
| Evaluation models (codenamed) | May underperform on security prompts; may change or vanish without notice |

### Retiring **2026-09-01** — migrate now

| Retiring | Replace with |
|---|---|
| `Claude Sonnet 4.5` | `Claude Sonnet 5` |
| `Claude Sonnet 4.6` | `Claude Sonnet 5` |
| `Claude Opus 4.5` | `Claude Opus 5` |
| `Claude Opus 4.6` | `Claude Opus 5` |
| `Gemini 3.1 Pro` | `Gemini 3.6 Flash` |
| `Raptor mini` | `MAI-Code-1-Flash` |

### Already retired — any pin to these is dead

| Retired model | Date | Replace with |
|---|---|---|
| `GPT-4.1` | 2026-06-01 | `GPT-5.5` |
| `GPT-5.2`, `GPT-5.2-Codex` | 2026-06-01 | `GPT-5.5` / `GPT-5.3-Codex` |
| `Grok Code Fast 1` | 2026-05-15 | `GPT-5 mini` |
| `Claude Sonnet 4` | 2026-05-01 | `Claude Sonnet 5` |
| `GPT-5.1` | 2026-04-15 | `GPT-5.3-Codex` |
| `GPT-5.1-Codex` / `-Max` / `-Mini` | 2026-04-01 | `GPT-5.3-Codex` |
| `Gemini 3 Pro` | 2026-03-26 | `Gemini 3.6 Flash` |
| `GPT-5`, `GPT-5-Codex`, `Claude Opus 4.1` | 2026-02-17 | `GPT-5.5` / `GPT-5.3-Codex` / `Claude Opus 5` |
| `Claude Sonnet 3.5` | 2025-11-06 | `Claude Haiku 4.5` |
| `Claude Opus 4`, `Claude Sonnet 3.7 (+Thinking)`, `Gemini 2.0 Flash`, `o1-mini`, `o3`, `o3-mini`, `o4-mini` | 2025-10-23 | See successor column in GitHub docs |
| `Gemini 2.5 Pro`, `Gemini 3 Flash` | 2026-07-31 | `Gemini 3.6 Flash` |

### Utility-only — never pin

`GPT-4o` · `GPT-4o mini` · `GPT-4.1` · `GPT-5.4 nano` — these power background features and are not
selectable in the model picker.

---

## 5. Remediation mapping for this suite

Apply with `python scripts/model_audit.py --fix` (writes proposed frontmatter changes; review the
diff before committing).

| Current pin in suite | Files | Status | Action |
|---|---:|---|---|
| `GPT-4.1` (all casings/quotings) | 30 | Retired 2026-06-01 | → task-class default; mostly specialist coding agents → `Claude Sonnet 5` |
| `GPT-5` / `gpt-5` | 18 | Retired 2026-02-17 | → `GPT-5.5`, or `Claude Sonnet 5` for coding agents |
| `Claude Sonnet 4.5` variants | 10 | **Retires 2026-09-01** | → `Claude Sonnet 5` — do these first |
| `Claude Sonnet 4.6` variants | 7 | **Retires 2026-09-01** | → `Claude Sonnet 5` — do these first |
| `Claude Sonnet 4` / `claude-sonnet-4` | 4 | Retired 2026-05-01 | → `Claude Sonnet 5` |
| `claude-3.5-sonnet` | 4 | Retired 2025-11-06 | → `Claude Haiku 4.5` (all four are Salesforce agents; volume work) |
| `gpt-4o`, `gpt-4` | 2 | Utility-only | → task-class default (utility pins are never selectable) |
| Malformed (list literal, `- GPT-4.1`, pipe-delimited ×2) | 4 | Invalid YAML scalar | → single valid string per task class |
| No pin | 142 | Undefined | → add pin per task class, prioritising T1 sub-orchestrators and high-traffic agents |

**Unpinned agents by proposed task class:** coding 60 · tests 23 · architecture 21 ·
orchestration 12 · docs 10 · codex-autonomy 10 · fast-interactive 6.

**Sequencing recommendation:** fix the 17 files retiring 2026-09-01 first (hard deadline), then the
58 retired pins, then the 142 unpinned agents in traffic order. Do not attempt all 225 in one PR.

---

## 6. Verification procedure

1. Run `python scripts/model_audit.py --report`.
2. Compare the model lists in Section 4 against the live GitHub supported-models page.
3. Update Section 4 and the `RETIRED` / `SUNSET` sets inside `scripts/model_audit.py` together —
   they must not diverge.
4. Record the verification date at the top of this file.
5. If a model in Section 3 has been retired, replace it in the task-class table **before** the
   retirement date, not after.
