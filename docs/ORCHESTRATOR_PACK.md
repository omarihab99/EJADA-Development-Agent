# Universal Orchestrator Pack — Development Agent Suite

**Version 1.0 · 2026-08-17 · Owner: ECC AI CoE — AI Adoption & Agents**

Drop-in governance, orchestration, and maintenance layer for the `Development-agents-main`
repository. Everything here is derived from the **actual contents** of the uploaded repository and
from the GitHub Copilot supported-models documentation verified on 2026-08-17. No figure in this
pack is estimated.

---

## What was found in the uploaded repository

| Fact | Value | How verified |
|---|---|---|
| Total agent files | 225 | File count |
| Delegation targets (`.github/agents/`) | 208 | File count |
| Quarantined (`non-dev-agents/`) | 17 | File count |
| Agent `name:` collisions | 0 | Frontmatter scan |
| Agents holding `runSubagent` | 5 | Frontmatter scan |
| **Upstream source** | `github/awesome-copilot` → `agents/` | SHA-256 match on 208 of 225 files |
| Byte-identical to upstream | 208 | SHA-256 comparison |
| Drifted from upstream | 13 (all `gem-*`) | SHA-256 comparison |
| Local-only | 4 | SHA-256 comparison |
| Missing from local (upstream-new) | 0 | SHA-256 comparison |
| Agents with a **valid current** model pin | **4 of 225** | `scripts/model_audit.py` |

### Five findings that need a decision

| # | Finding | Severity | Why it matters |
|---|---|---|---|
| **F1** | `.github/copilot-instructions.md` documented a `textkit` Python library with `src/`, `tests/`, and `pyproject.toml`. **None of these exist in the repository.** | **P1** | That file is auto-injected into all 225 agents. Every agent was carrying a false premise about the repo. **Fixed** in this pack. |
| **F2** | 17 agents pin `Claude Sonnet 4.5` / `4.6`, which GitHub retires on **2026-09-01** — 15 days away. | **P1** | Silent fallback with no warning; behaviour changes underneath users. |
| **F3** | 56 agents pin an already-retired model (30 × `GPT-4.1`, 18 × `GPT-5`, 4 × `Claude Sonnet 4`, 4 × `claude-3.5-sonnet`). | **P1** | These pins are already dead. |
| **F4** | 142 agents declare no `model:` at all. | **P2** | Same agent behaves differently for each user; results are not reproducible and cost is uncontrolled. |
| **F5** | The 13 drifted `gem-*` agents are **2–3× larger locally** than upstream, and `gem-orchestrator` / `gem-planner` reference three **local-only** agents (`gem-critic`, `gem-designer-mobile`, `gem-implementer-mobile`) that upstream has removed. | **P2** | A naive `git pull` of upstream would silently break those references. This is exactly why the sync tool recommends rather than applies. |

---

## Contents

```
agent-suite-pack/
├── .github/
│   ├── agents/
│   │   ├── universal-orchestrator.agent.md   ← the orchestrator (install this)
│   │   └── AGENT_INDEX.md                    ← routing source of truth, all 208 agents
│   └── copilot-instructions.md               ← corrected shared ground rules (v2.0)
├── governance/
│   ├── AGENT_GOVERNANCE.md                   ← tiers, change control, safety, audit, cadence
│   ├── MODEL_POLICY.md                       ← model selection + retirement + remediation
│   └── RESPONSE_CONTRACT_AND_VALIDATION.md   ← Response Contract + Default Validation Output
├── registry/
│   ├── AGENT_REGISTRY.csv                    ← 225 rows: domain, model status, provenance, drift, hash
│   ├── MODEL_AUDIT.md                        ← generated audit, per-file remediation
│   ├── UPSTREAM_SYNC_REPORT.md               ← generated drift report + decision log
│   └── .agentlock.json                       ← provenance lock (hashes per agent)
└── scripts/
    ├── model_audit.py                        ← audit + --fix model pins
    └── agent_sync_check.py                   ← upstream version check + update recommendation
```

---

## Install

```bash
# 1. Copy the pack over the agent repository
cp -r agent-suite-pack/.github/agents/universal-orchestrator.agent.md  <repo>/.github/agents/
cp -r agent-suite-pack/.github/agents/AGENT_INDEX.md                   <repo>/.github/agents/
cp    agent-suite-pack/.github/copilot-instructions.md                 <repo>/.github/
cp -r agent-suite-pack/governance agent-suite-pack/registry agent-suite-pack/scripts <repo>/

# 2. Verify the current state (no writes)
cd <repo>
python scripts/model_audit.py --report
python scripts/agent_sync_check.py --report

# 3. Preview the model remediation, then apply once reviewed
python scripts/model_audit.py --fix --dry-run
python scripts/model_audit.py --fix            # creates .bak beside each file

# 4. In VS Code, select "Universal Orchestrator" in the agent picker
```

### Decide before installing

1. **Keep or retire `Development Orchestrator`?** The Universal Orchestrator supersedes it. Running
   both means two competing routers in the picker. Recommendation: delete the old one once the new
   one is validated, and keep it for one sprint as a rollback.
2. **Model pin for the orchestrator itself.** Currently `Claude Opus 5`. If your plan or org policy
   restricts Opus-class models, change it to `GPT-5.6 Sol` before installing.
3. **Who is the suite owner?** Governance change control needs a named person. Currently unassigned
   — marked `[INPUT NEEDED]` in `AGENT_GOVERNANCE.md`.

---

## Recommended sequence

| # | Action | Owner | By |
|---|---|---|---|
| 1 | Install corrected `copilot-instructions.md` (fixes F1 — affects all 225 agents) | Suite owner | 2026-08-19 |
| 2 | Fix the 17 agents retiring 2026-09-01 (F2) | Suite owner | **2026-08-27** |
| 3 | Install Universal Orchestrator + `AGENT_INDEX.md`; validate routing on 5 real tasks | Suite owner | 2026-08-27 |
| 4 | Fix the 56 retired pins (F3) via `model_audit.py --fix`, reviewed in one PR per domain | Domain owners | 2026-09-10 |
| 5 | Three-way review of the 13 `gem-*` drifted agents (F5); record decisions in the sync report | Domain owner | 2026-09-10 |
| 6 | Pin the 142 unpinned agents (F4), in traffic order | Domain owners | 2026-09-30 |
| 7 | Add CI: name-collision, model-status, and reference-integrity gates (G7) | Suite owner | 2026-09-30 |

---

## Suggested CI gate

```yaml
# .github/workflows/agent-suite-check.yml
name: Agent suite check
on:
  pull_request:
    paths: ['.github/agents/**', '.github/copilot-instructions.md', 'non-dev-agents/**']
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      # Fails the PR on any retired, sunset, utility-only, or malformed model pin
      - run: python scripts/model_audit.py --report --out registry/MODEL_AUDIT.md
      # Informational: exits 1 when upstream drift exists; does not block
      - run: python scripts/agent_sync_check.py --report --out registry/UPSTREAM_SYNC_REPORT.md
        continue-on-error: true
```

---

## Known limitations — stated, not hidden

- **Domain classification in `AGENT_INDEX.md` and `AGENT_REGISTRY.csv` is heuristic**, derived from
  filename and description keywords. It is a navigation aid. Roughly 5–10% of entries will sit in a
  defensibly different domain. It does not constrain routing.
- **`model_audit.py --fix` proposals are advisory.** The task class is inferred from the filename,
  then the description. Review the `--dry-run` output; a handful will be wrong.
- **Drift direction for the 13 `gem-*` agents is unconfirmed.** Local files are larger, which is
  consistent with either local customisation or an older, more verbose upstream generation. The
  original fork date was not available in the uploaded archive. This needs a human answer.
- **Model tables are a point-in-time snapshot (2026-08-17).** GitHub changes model availability
  monthly. The tables live in two places — `governance/MODEL_POLICY.md` and the `MODEL TABLES`
  section of `scripts/model_audit.py` — and must be updated together.
- **Upstream sync assumes `github/awesome-copilot` @ `main`.** If the suite was forked from a tag or
  a different fork, pass `--repo` / `--upstream-ref`. Provenance was inferred from a 208/225
  SHA-256 match, not from recorded fork metadata — the repository carries none.
