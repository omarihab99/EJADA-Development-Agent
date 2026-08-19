# Response Contract & Default Validation Output

**Version 1.0 · 2026-08-17**
Applies to the Universal Orchestrator and to any agent producing a decision-grade artifact.

---

## Part A — Response Contract

Three tiers. The orchestrator selects the tier based on request complexity; the selected tier is
stated in the routing block. Higher tiers include all sections from lower tiers.

### Tier selection

| Tier | When to use | Required sections |
|---|---|---|
| **Compact** | Trivial / single-domain / advisory / no file changes | 1 Assigned Agent, 2 On-the-spot answer |
| **Standard** | Moderate complexity, file changes, or follow-up work | 1–5 (add Handoff Prompt, Artifact Pack, Next Actions) |
| **Full** | Multi-agent, governance, regulated, production, or multi-stakeholder work | 1–6 (add Tracker Update) |

Mark unused optional sections `N/A` rather than dropping them, so omissions stay visible.

### Template

```markdown
### 1. Assigned Agent
<exact agent name(s) + one clause on why each. "Handled directly" is valid.
 Disclose any model substitution here: "ran on Claude Sonnet 5 — the agent's GPT-4.1 pin is retired".>

### 2. On-the-spot answer
<the substance: decision, code, analysis, finding. Lead with the answer, not the method.>

### 3. Handoff Prompt
<copy-paste-ready, self-contained brief for the next agent or person:
 CONTEXT / TASK / MUST NOT / ACCEPTANCE / RETURN FORMAT>

### 4. Artifact Pack
| Artifact | Path | Status | Notes |
|---|---|---|---|

### 5. Next Actions
1. <action> — Owner: <name> — By: <explicit date>

### 6. Tracker Update
| Completed | Open | Owner | Evidence/Artifact | Risk/Blocker | Ask | Next step |
|---|---|---|---|---|---|---|
```

### Section rules

| Section | Include when | Omit / N/A when |
|---|---|---|
| 1. Assigned Agent | Always | Never |
| 2. On-the-spot answer | Always | Never |
| 3. Handoff Prompt | Work continues with another agent or person | The task is closed |
| 4. Artifact Pack | Any file created or changed | Advisory answer only |
| 5. Next Actions | Anything remains open | Fully closed, nothing pending |
| 6. Tracker Update | Multi-step or multi-stakeholder work | One-shot answer with no tracking value |

### Anti-patterns

- Restating Section 2 inside Sections 3–6.
- Vague dates ("soon", "next week"). Use explicit dates.
- Unowned actions. Every action has a named owner.
- Padding Section 4 with files that were only read.
- Hiding a model substitution.

---

## Part B — AI Validation Framework

Score each dimension `Strong / Adequate / Weak / Unknown`. `Unknown` is preferred over a guess.

| # | Dimension | Test |
|---|---|---|
| 1 | AI Fit | Genuine AI/GenAI/RAG/agent/Copilot value, or ordinary automation wearing an AI label? |
| 2 | Business Value | Time saved, effort reduced, quality raised, decision support, governance gain? |
| 3 | Feasibility | Realistic given available tools, data, owners, SMEs, and process readiness? |
| 4 | Data Readiness | Do the templates, docs, tickets, code, logs, dashboards, examples actually exist and are they accessible? |
| 5 | Governance | Human review point, SME validation, access control, privacy, Responsible AI, approval path? |
| 6 | Reuse Potential | Reusable asset, prompt pack, workflow, RAG assistant, or agent? |
| 7 | Pilot Readiness | Ready to pilot, needs elaboration, or reject/defer? |

### Decisions — use exactly one

| Decision | Use when |
|---|---|
| **Accepted Idea** | AI fit is real, value is articulable, data exists, an owner exists, governance path is clear |
| **More Elaboration Needed** | The idea is plausible but a named input is missing — data, owner, process, or scope |
| **Not Accepted Idea** | No genuine AI fit, no value case, no data, no owner, or the governance path is closed |

**Do not invent a fourth decision.** "Accepted with conditions" is `More Elaboration Needed` with
the conditions named in `Validation Notes`.

---

## Part C — Default Validation Output

One row per item. Column order is fixed.

| # | Column | Rule |
|---|---|---|
| 1 | Validation Feedback | One of the three decisions, exactly |
| 2 | Validation Detail | 1–2 sentences, specific to this item, on why |
| 3 | Validation Notes | Caveats, dependencies, conditions |
| 4 | Reality / Doability | Blunt practical assessment; name the binding constraint |
| 5 | Suggestion for How to Apply | Concrete first implementation step or pattern |
| 6 | Missing Inputs | Named required items, or `None` |
| 7 | Recommended AI Approach | Copilot agent / RAG / prompt pack / fine-tune / classic automation / none |
| 8 | Owner / SME Follow-up | Named role or person, and what for |
| 9 | Pilot Readiness | `Ready` / `Needs elaboration` / `Not ready` + the single gating item |
| 10 | Governance Notes | Human review point, data sensitivity, access control, audit requirement |

### Comment rules

- Short, practical, business-readable, **row-specific**.
- Never paste a generic comment across rows.
- Never invent missing data — name it in `Missing Inputs`.
- Strict but constructive: if rejecting, say what would change the answer.

### Worked example (from this suite's own audit)

| Column | Value |
|---|---|
| Validation Feedback | More Elaboration Needed |
| Validation Detail | Adopting all 13 upstream `gem-*` updates is plausible, but the direction of drift is unconfirmed — local files are 2–3× larger than upstream, which may be local customisation or an older upstream generation. |
| Validation Notes | `gem-orchestrator` embeds an explicit child-agent list that includes three local-only agents. Taking upstream deletes those references. |
| Reality / Doability | Doable, but not as a bulk update. Binding constraint is the child-agent reference graph, not the file content. |
| Suggestion for How to Apply | Three-way diff one agent (`gem-planner`) first, decide keep/take/merge, then apply the same decision pattern to the remaining 12. |
| Missing Inputs | Original fork date; whether the local `gem-*` edits were deliberate; owner of the `gem-*` family. |
| Recommended AI Approach | None — this is a source-control and change-management task, not an AI task. |
| Owner / SME Follow-up | Suite owner — confirm whether local `gem-*` edits were intentional. |
| Pilot Readiness | Needs elaboration — gated on confirming drift direction. |
| Governance Notes | Change-controlled: `.github/agents/**` edits affect all users. Record the decision in `registry/UPSTREAM_SYNC_REPORT.md`. |

---

## Part D — Report formats

### AI adoption progress report

1. YTD Achievements
2. Current Focuses
3. Key Asks
4. Main Risks
5. Next Actions

### AI validation report

1. Validation Scope
2. Accepted Ideas
3. More Elaboration Needed
4. Not Accepted Ideas
5. Missing Inputs
6. Owner / SPOC Follow-ups
7. Risks / Blockers
8. Next Actions
9. Tracker Update
