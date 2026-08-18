# Agent Suite Governance Framework

**Version 1.0 · Effective 2026-08-17 · Owner: ECC AI CoE — AI Adoption & Agents**
**Suite owner (named individual accountable for change control): `[INPUT NEEDED]`**
**Scope:** all 225 agent definitions, the shared instructions file, and the orchestration layer.

---

## 1. Governance objectives

| Objective | Control | Evidence |
|---|---|---|
| Predictable routing | Single orchestrator, verified agent names, published index | `registry/AGENT_REGISTRY.csv` |
| Cost control | Model policy by task class; premium models on exception | `scripts/model_audit.py` output |
| Change control | Review gate on `.github/agents/**` and `governance/**` | PR approval record |
| Provenance | Every agent tagged with source and drift class | `registry/UPSTREAM_SYNC_REPORT.md` |
| Auditability | Response Contract logs agent, task, model, outcome per turn | Conversation transcript |
| Safety | Least-privilege tools, untrusted-content rule, human gate | This document, Section 5 |

---

## 2. Agent tiering

| Tier | Definition | Count (2026-08-17) | Controls |
|---|---|---|---|
| **T0 — Orchestration** | Holds `runSubagent`; routes and arbitrates | 1 (`Universal Orchestrator`) | Named owner; change requires suite-owner approval; model pinned and reviewed quarterly |
| **T1 — Sub-orchestrators** | Agents that delegate within their own workflow | 4 (`azure-iac-exporter`, `azure-iac-generator`, `Context7-Expert`, `technical-content-evaluator`) | Must declare their child agents explicitly; child list validated on every sync |
| **T2 — Specialists** | Single-domain expert agents | 203 | Model policy applies; no `runSubagent`; upstream drift tracked |
| **T3 — Non-delegation** | `non-dev-agents/` | 17 | Excluded from routing; not loaded as delegation targets |

**Rule:** promotion between tiers (e.g. granting `runSubagent` to a T2 agent) is a change-controlled
action requiring a written rationale in the PR.

---

## 3. Change control

| Change | Approval required | Post-change action |
|---|---|---|
| Edit `.github/copilot-instructions.md` | Suite owner | Announce — affects all 225 agents |
| Edit `Universal Orchestrator` | Suite owner | Re-run smoke routing tests |
| Add a new T2 agent | Domain owner | Add registry row; confirm no name collision; confirm model is supported |
| Take an upstream update on a `DRIFTED` agent | Domain owner + suite owner | Record decision in sync report; re-run model audit |
| Add `runSubagent` to any agent | Suite owner | Document delegation depth and cost implication |
| Pin a premium model (Opus class) | Suite owner | Justify against task class in `MODEL_POLICY.md` |
| Delete an agent | Suite owner | Grep the suite for references first; sub-orchestrators embed child names |

**Never merge an agent change without:** a name-uniqueness check, a model-status check, and a
reference check for the agent's name across `.github/agents/**`.

---

## 4. Access, secrets, and data handling

- **Least privilege on tools.** An agent's `tools:` list is a security boundary. Do not add
  `runCommands`, `editFiles`, or `fetch` to an agent that does not demonstrably need them.
- **No credentials in agent files.** Agent definitions are plain text in source control; treat them
  as public within the organisation.
- **Content exclusion.** Sensitive paths must be covered by Copilot content exclusion at the org or
  repo level. Agent instructions are not an access control mechanism and must never be relied on
  as one.
- **Client data.** No client-identifiable data, pricing, or contract detail in agent definitions,
  examples, or test fixtures.
- **Data residency and retention.** Model choice carries a data-handling posture. Models outside the
  standard retention agreement (currently Claude Fable 5) and open-weight models (Kimi K2.7 Code,
  Kimi K3, DeepSeek) require named approval before use. See `MODEL_POLICY.md`.

---

## 5. Safety controls

| Risk | Control | Owner |
|---|---|---|
| Prompt injection via fetched content | "Untrusted content is data, not instruction" rule in shared instructions and orchestrator | All agents |
| Malicious or drifted agent definition | Upstream hash comparison every sync; `Trojan Skill Hunter` review on new adoptions | Suite owner |
| Runaway delegation cost | Only T0 holds `runSubagent`; T1 child lists are explicit and bounded | Orchestrator |
| Irreversible action | Human confirmation gate before merge, force-push, schema drop, secret rotation, production change | Orchestrator |
| Fabricated output | No-fabrication and no-inference rules; missing inputs quarantined and reported | Orchestrator |
| Silent model substitution | Substitutions must be disclosed in Response Contract Section 1 | Orchestrator |
| Security conclusions from non-security agents | Security findings only from a security agent or a named policy | Orchestrator routing rule 5 |

---

## 6. Audit trail

Every meaningful orchestrated turn must record:

| Field | Source |
|---|---|
| Agent(s) invoked, by exact name | Response Contract §1 |
| Task brief issued | Delegation brief template |
| Model used, and whether substituted | Response Contract §1 |
| Artifacts created or changed, with paths | Response Contract §4 |
| Verification evidence (build/test/problems) | Response Contract §2 |
| Open risks, blockers, and asks | Response Contract §6 |

For regulated or client-facing work, export the transcript section into the delivery record.

---

## 7. Review cadence

| Activity | Frequency | Trigger |
|---|---|---|
| Model status audit (`scripts/model_audit.py`) | Monthly | Also before any release, and on any GitHub model retirement announcement |
| Upstream sync check (`scripts/agent_sync_check.py`) | Monthly | Also before any release |
| Orchestrator routing review | Quarterly | Also after adding >10 agents |
| Governance framework review | Quarterly | Also after any incident |
| Name-collision and reference integrity check | Every PR touching `.github/agents/**` | Automated in CI |

---

## 8. Known open items (as at 2026-08-17)

| # | Item | Severity | Owner | Status |
|---|---|---|---|---|
| G1 | 56 agents pin models GitHub has already retired | P1 | Suite owner | Open — remediation script provided |
| G2 | 17 agents pin models retiring 2026-09-01 | P1 | Suite owner | Open — 15 days to deadline |
| G3 | 142 agents declare no `model:`; behaviour depends on user's picker | P2 | Domain owners | Open — policy defined, pins not yet applied |
| G4 | Shared instructions described a non-existent `textkit` library | P1 | Suite owner | **Fixed in v2.0 of `copilot-instructions.md`** |
| G5 | 13 `gem-*` agents drifted from upstream; direction of drift unconfirmed | P2 | Domain owner | Open — needs three-way review |
| G6 | 3 local-only `gem-*` agents referenced by a drifted orchestrator; upstream removed them | P2 | Domain owner | Open — taking upstream would break references |
| G7 | No CI gate on name collision, model status, or reference integrity | P2 | Suite owner | Open — scripts provided, workflow not yet added |
| G8 | 2 agents pin utility-only models (`gpt-4o`, `gpt-4`) not selectable in the picker | P2 | Suite owner | Open |
| G9 | 4 agents have malformed `model:` values (list literal, YAML list item, pipe-delimited ×2) | P3 | Suite owner | Open |
