# Production Alignment Notes

This bundle aligns the runtime control files around one rule: governance is proportional to risk.

## Runtime behavior
- Fast Path: no registry/model/governance load unless specifically required.
- Single-Specialist: default development path, agent-first, one delegation, Low/Medium work proceeds without approval under balanced profile.
- High Risk: full governance and exact approval immediately before gated action.
- Model policy is lazy: a valid supported allowed pin does not require policy/benchmark loading for routine execution.
- Response output is proportional and avoids routine routing/model/governance ceremony.

## Important registry observation
The supplied registry contains retired, utility-only, unpinned, and drifted entries. This bundle intentionally does not mass-edit registry rows without regenerating them from actual agent frontmatter and current support verification. Run the repository model/registry audit before production release.
