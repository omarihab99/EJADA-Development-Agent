# Upstream Sync Report

**Generated:** 2026-08-17  
**Upstream:** `github/awesome-copilot` @ `main` (`agents/`)  
**Local scope:** .github/agents

## Summary

| Drift class | Count | Recommendation |
|---|---:|---|
| `IDENTICAL` | 191 | No action. Safe to auto-update on the next upstream change. |
| `DRIFTED` | 13 | REVIEW — three-way diff required. Do not bulk-overwrite; local edits may be deliberate. |
| `LOCAL-ONLY` | 4 | Exclude from sync. Confirm nothing upstream supersedes it. |
| `QUARANTINED` | 17 | Held in non-dev-agents/ by design. Do not move into .github/agents/. |

## Requires human decision — DRIFTED

| File | Agent name | Local bytes | Upstream bytes | Delta | References |
|---|---|---:|---:|---:|---|
| `gem-browser-tester.agent.md` | gem-browser-tester | 6560 | 3572 | +2988 | — |
| `gem-code-simplifier.agent.md` | gem-code-simplifier | 6700 | 4054 | +2646 | — |
| `gem-debugger.agent.md` | gem-debugger | 7785 | 4119 | +3666 | — |
| `gem-designer.agent.md` | gem-designer | 10733 | 4211 | +6522 | — |
| `gem-devops.agent.md` | gem-devops | 8176 | 3234 | +4942 | — |
| `gem-documentation-writer.agent.md` | gem-documentation-writer | 9292 | 2420 | +6872 | — |
| `gem-implementer.agent.md` | gem-implementer | 5988 | 5669 | +319 | — |
| `gem-mobile-tester.agent.md` | gem-mobile-tester | 7387 | 3447 | +3940 | — |
| `gem-orchestrator.agent.md` | gem-orchestrator | 21486 | 17663 | +3823 | `gem-browser-tester`, `gem-code-simplifier`, `gem-critic`, `gem-debugger`, `gem-designer`, `gem-designer-mobile` |
| `gem-planner.agent.md` | gem-planner | 21755 | 9469 | +12286 | `gem-browser-tester`, `gem-code-simplifier`, `gem-critic`, `gem-debugger`, `gem-designer`, `gem-designer-mobile` |
| `gem-researcher.agent.md` | gem-researcher | 7426 | 4565 | +2861 | — |
| `gem-reviewer.agent.md` | gem-reviewer | 8164 | 6640 | +1524 | — |
| `gem-skill-creator.agent.md` | gem-skill-creator | 7576 | 4260 | +3316 | — |

> A large positive delta usually means local customisation or an older, more verbose upstream generation. Confirm the direction before taking upstream.


## Local-only agents (excluded from sync)

| File | Agent name | Referenced by |
|---|---|---|
| `development-orchestrator.agent.md` | Development Orchestrator | — (orphan) |
| `gem-critic.agent.md` | gem-critic | `gem-orchestrator.agent.md`, `gem-planner.agent.md` |
| `gem-designer-mobile.agent.md` | gem-designer-mobile | `development-orchestrator.agent.md`, `gem-orchestrator.agent.md`, `gem-planner.agent.md` |
| `gem-implementer-mobile.agent.md` | gem-implementer-mobile | `development-orchestrator.agent.md`, `gem-orchestrator.agent.md`, `gem-planner.agent.md` |

## Decision log

| Date | File | Drift | Decision | Decided by |
|---|---|---|---|---|
| | | | | |

> Record every take-upstream / keep-local / merge decision here before merging.

## Post-sync checklist

- [ ] Re-run `python scripts/model_audit.py --report` — upstream files carry upstream model pins
- [ ] Verify no sub-orchestrator lost a child-agent reference
- [ ] Verify agent `name:` uniqueness across the suite
- [ ] Update `registry/AGENT_REGISTRY.csv`
