# Repository Index

**Purpose:** durable navigation map for the Development Agent Suite. This file reduces repeated repository discovery. It is guidance and must not be treated as proof that file contents are unchanged.

## Core components

- `.github/agents/universal-orchestrator.agent.md`: main governed coordinator.
- `.github/agents/*.agent.md`: development specialists (includes the local-only `ef-core-expert.agent.md` for EF Core / migrations).
- `.github/agents/AGENT_INDEX.md`: generated agent lookup (view of the registry).
- `.github/copilot-instructions.md`: concise shared repository rules.
- `governance/AGENT_GOVERNANCE.md`: risk, approval, safety, and change controls.
- `governance/MODEL_POLICY.md`: model resolution and fallback policy.
- `governance/RESPONSE_CONTRACT_AND_VALIDATION.md`: response tiers and validation format.
- `registry/AGENT_REGISTRY.csv`: agent identity, domain, lifecycle, provenance, and model status.
- `registry/MODEL_AUDIT.md`: generated maintenance report.
- `registry/UPSTREAM_SYNC_REPORT.md`: generated upstream drift report.
- `scripts/model_audit.py`: model audit and proposed remediation.
- `scripts/agent_sync_check.py`: upstream comparison and drift reporting.
- `scripts/registry_build.py`: regenerates `registry/AGENT_REGISTRY.csv` and `AGENT_INDEX.md` from the agent files (`--check` for CI).
- `scripts/restore_copilot_instructions.py`: restores the shared instructions from git when missing.
- `tests/test_agent_suite_integrity.py`: static integrity tests (front matter, registry, delegation allowlist, links).
- `.github/workflows/agent-integrity.yml`: CI that runs the tests and the registry check.
- `non-dev-agents/`: agents excluded from development delegation.

## Runtime loading order

1. Use current-execution context.
2. Use this index.
3. Check changed files.
4. Read only likely target files and direct dependencies.
5. Expand discovery only when evidence is insufficient.

## Update triggers

Update this index only when:
- A key path is added, removed, renamed, or moved.
- A component responsibility changes.
- Build, test, audit, or synchronization commands change.
- The supported entry point or governance structure changes.

Do not update it for ordinary content edits that do not change navigation or responsibility.

## Known execution paths

- **Direct (Fast) Path:** only for requests with no registered specialist domain; no delegation.
- **Single-Specialist Path:** one verified specialist for focused single-domain work.
- **Orchestrated Path:** up to three specialists by default for multi-domain or high-risk work.

## Validation commands

Confirm commands against the current repository before relying on them:

```bash
python -m pytest -q tests                  # executed 2026-10-01: 464 passed
python scripts/registry_build.py --check   # executed 2026-10-01: up to date
python scripts/model_audit.py --report
python scripts/agent_sync_check.py --report
```

Add project-specific build, lint, test, and agent-definition validation commands here only after they are executed successfully in the repository.
