# Upstream Sync Report

**Generated:** 2026-08-19  
**Upstream:** `github/awesome-copilot` on `main`  
**Local scope:** `.github/agents`

## Baseline summary

The supplied 2026-08-17 report recorded 191 identical, 13 drifted, 4 local-only, and 17 quarantined definitions. Re-run the sync check before using these counts as current.

## Decision policy

A difference is not automatically an update or a defect. For every drifted agent, choose exactly one:

- **Keep local:** local customization is intentional and remains supported.
- **Take upstream:** upstream is authoritative and local behavior is no longer required.
- **Merge:** both contain required behavior; reconcile explicitly.
- **Quarantine:** safety, provenance, or ownership is unresolved.

## Required three-way review

Compare merge base, local, and current upstream. Review frontmatter, model, tools, instructions, child-agent references, output contract, safety rules, and tests. A byte-size delta is a triage signal only, never a decision rationale.

## Decision record

| Date | File | Agent | Base commit | Upstream commit | Drift summary | Reference impact | Decision | Rationale | Owner | Approver | Tests/evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Blocking conditions

Block sync when:

- drift direction or owner is unknown;
- the agent is referenced by an orchestrator and a rename/delete would break routing;
- upstream adds broader tools, delegation, or a premium/invalid model without local approval;
- local content contains credentials or client-identifiable data;
- name uniqueness, model status, or reference integrity checks fail;
- no rollback point or representative regression test exists.

## Post-sync checklist

- [ ] Re-run model audit.
- [ ] Verify exact agent-name uniqueness.
- [ ] Verify all child-agent and routing references.
- [ ] Confirm tools still satisfy least privilege.
- [ ] Run secret and sensitive-data checks.
- [ ] Run representative behavioral and routing tests.
- [ ] Update `registry/AGENT_REGISTRY.csv`.
- [ ] Record the decision and evidence above.
- [ ] Confirm owner approval and rollback point.
