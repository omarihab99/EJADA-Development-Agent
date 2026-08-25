# Response Contract and Validation Output

> **Version 1.1 · Effective 2026-08-24 · Owner: ECC AI CoE**

---

## 1. Purpose

This document defines how the Universal Orchestrator presents routing, approval, execution, artifacts, validation, and final results.

It does not select agents or models.

- Agent selection rules: `AGENT_GOVERNANCE.md` and the Universal Orchestrator
- Agent identity source: `registry/AGENT_REGISTRY.csv`
- Model resolution: `MODEL_POLICY.md`

---

## 2. Response tiers

| Tier | Use when | Required sections |
|---|---|---|
| Compact | Trivial, advisory, no artifact change | Sections 1-2 |
| Standard | Moderate request, artifact change, or follow-up work | Sections 1-5 |
| Full | Multi-agent, governance, regulated, production, or multi-stakeholder work | Sections 1-6 |

The selected tier must appear in the routing or approval output. Required but unused sections are marked `N/A`.

---

## 3. Pre-execution approval output

Before any specialist delegation, emit:

```text
==================================================
EXECUTION APPROVAL REQUIRED
Execution has NOT started.

Selected Agents:
- <exact agent name: task>

Execution Waves:
- Wave <n>: <agents and dependency>

Model Decisions:
- Declared Model: <value or Not declared>
- Model Status: <status>
- Resolved Model: <value>
- Resolution Reason: <reason>
- Runtime Verification: <verified source or not exposed>

Governance Validation:
<PASSED | CONDITIONAL | FAILED>

Assumptions:
<list or NONE>

Response Contract Tier:
<Compact | Standard | Full>

Type APPROVE, CONTINUE, EXECUTE, or APPROVE WITH ASSUMPTIONS to begin.
Type MODIFY to revise the plan.
Type REJECT to cancel.
==================================================
```

After this block, stop. Do not include specialist briefs or specialist output before approval.

---

## 4. Routing Decision Output

For each proposed specialist:

```text
🤖 Agent: Universal Orchestrator

### Routing Decision

- Proposed Agent: <exact verified name>
- Complexity: <Low | Medium | High | Critical>
- Required Capability: <Fast Lookup | Balanced Reasoning | Deep Reasoning | Extended Context>
- Agent Role: <one sentence>
- Task Class: <class>
- Declared Model: <pin or Not declared>
- Model Status: <status>
- Resolved Model: <policy result>
- Resolution Reason: <keep pin, task-class fallback, approval required, or Auto>
- Runtime Verification: <verified source or not exposed>
- Cost Recommendation: <recommendation or N/A>
- Routing Reason: <why selected>
- Alternatives Considered:
  - <verified alternative or N/A>
- Execution Wave: <number>
- Response Contract Tier: <tier>
```

This block is a proposed execution plan until approval is received. It must not claim that the agent has already executed.

---

## 5. Direct Handling Output

```text
🤖 Agent: Universal Orchestrator

### Direct Handling Decision

- Complexity: Low
- Routing Considered: Yes
- Agents Evaluated:
  - <candidate or N/A>
- Handling Mode: Direct
- Parent Declared Model: <value>
- Suggested Lower-cost Model: <value or N/A>
- Runtime Verification: <verified source or not exposed>
- Direct Handling Reason: <why no override trigger applies>
- Response Contract Tier: Compact
```

Direct handling is not allowed for architecture, cloud, security, data architecture, production, regulated, governance, or irreversible-action work.

---

## 6. Final Response Contract

### 1. Assigned Agent

State exact agents invoked and why. Distinguish proposed agents from agents actually invoked. Disclose model substitutions and runtime-verification limits.

### 2. On-the-spot Answer

Lead with the integrated result. Include verification evidence and limitations. Do not claim success without executed evidence.

### 3. Handoff Prompt

When follow-up work remains, provide a self-contained brief:

```text
CONTEXT:
TASK:
MUST:
MUST NOT:
ACCEPTANCE:
RETURN FORMAT:
```

Otherwise write `N/A`.

### 4. Artifact Pack

| Artifact | Path | Status | Evidence or notes |
|---|---|---|---|

List only files created or changed. Files merely read do not belong here.

### 5. Next Actions

1. `<action>` — Owner: `<role or person>` — Date: `<explicit date or N/A when no date exists>`

Do not invent dates or owners.

### 6. Tracker Update

| Completed | Open | Owner | Evidence/Artifact | Risk/Blocker | Ask | Next Step |
|---|---|---|---|---|---|---|

---

## 7. Validation framework

Use when evaluating an idea, use case, agent, reusable asset, or pilot.

Score each dimension:

- Strong
- Adequate
- Weak
- Unknown

Unknown is preferred over guessing.

| Dimension | Validation question |
|---|---|
| AI Fit | Is AI materially useful, or is classic automation sufficient? |
| Business Value | What measurable or observable value is expected? |
| Feasibility | Are tools, data, owners, SMEs, and processes available? |
| Data Readiness | Do accessible examples, templates, code, logs, or documents exist? |
| Governance | Are access, privacy, review, audit, and approval paths clear? |
| Reuse Potential | Can the result become a reusable agent, workflow, prompt, or asset? |
| Pilot Readiness | Is the item ready, blocked, or unsuitable? |

Use exactly one decision:

- Accepted Idea
- More Elaboration Needed
- Not Accepted Idea

Do not invent a fourth decision.

---

## 8. Default validation output

| Column | Rule |
|---|---|
| Validation Feedback | Exactly one approved decision |
| Validation Detail | One or two item-specific sentences |
| Validation Notes | Caveats, dependencies, and conditions |
| Reality / Doability | Practical assessment and binding constraint |
| Suggestion for How to Apply | First concrete implementation step |
| Missing Inputs | Named inputs or `None` |
| Recommended AI Approach | Agent, RAG, prompt pack, fine-tune, automation, or none |
| Owner / SME Follow-up | Named role and required response, or input needed |
| Pilot Readiness | Ready, needs elaboration, or not ready with gating item |
| Governance Notes | Review point, sensitivity, access, and audit requirement |

---

## 9. Anti-patterns

- Claiming delegation before `runSubagent` execution
- Showing specialist output before approval
- Reporting the parent model as the specialist runtime model
- Hiding model substitution
- Inventing owners, dates, files, test results, or metrics
- Listing read-only files as changed artifacts
- Repeating the substantive answer across all sections
