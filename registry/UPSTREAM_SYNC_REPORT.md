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
| 2026-10-01 | arch.agent.md | Senior Cloud Architect | n/a (not recorded) | n/a (upstream unreachable during audit) | Model pin Claude Opus 5 added before the 2026-10-01 audit | Delegation target unchanged | Keep local | Pre-existing local pin; premium-pin reason not recorded, owner review required | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | azure-iac-exporter.agent.md | azure-iac-exporter | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | azure-iac-generator.agent.md | azure-iac-generator | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | azure-verified-modules-owner-triage.agent.md | AVM Owner Triage | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | context7.agent.md | Context7-Expert | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | custom-agent-foundry.agent.md | Custom Agent Foundry | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | declarative-agents-architect.agent.md | Declarative Agents Architect | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: invalid model pin removed; description added | Delegation target unchanged | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | dotnet-self-learning-architect.agent.md | .NET Self-Learning Architect | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: malformed model removed; delegation tool removed | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | laravel-expert-agent.agent.md | Laravel Expert Agent | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: invalid model pin removed | Delegation target unchanged | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | modernization.agent.md | Modernization Agent | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | new-relic-incident-response.agent.md | New Relic Incident Response Agent | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: invalid model pin removed | Delegation target unchanged | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | pimcore-expert.agent.md | Pimcore Expert | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: invalid model pin removed | Delegation target unchanged | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | principal-software-engineer.agent.md | Principal software engineer | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | python-notebook-sample-builder.agent.md | Python Notebook Sample Builder | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | qa-subagent.agent.md | QA | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | research-technical-spike.agent.md | Technical spike research mode | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | salesforce-expert.agent.md | Salesforce Expert Agent | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | se-security-reviewer.agent.md | SE: Security | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: tools line repaired (UI residue) | Delegation target unchanged | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | swe-subagent.agent.md | SWE | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | technical-content-evaluator.agent.md | technical-content-evaluator | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | terraform-aws-implement.agent.md | terraform-aws-implement | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |
| 2026-10-01 | terraform-azure-implement.agent.md | Azure Terraform IaC Implementation Specialist | n/a (not recorded) | n/a (upstream unreachable during audit) | Front matter: delegation tool removed (D5) | Agent can no longer call subagents; body references reviewed in notes | Keep local | Governance/metadata correction approved 2026-10-01 | Moaiad | Moaiad | tests/test_agent_suite_integrity.py |

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
