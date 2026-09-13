# Repository Discovery Policy

## Goal

Identify the correct files without requiring the user to mention them and without repeatedly scanning the whole repository.

## Discovery order

1. Reuse files and findings already collected during the current execution.
2. Read `.ai/repository-index.md` when present.
3. Inspect the changed-file list and repository manifests.
4. Search by concrete feature names, symbols, errors, tables, endpoints, report names, components, or configuration keys.
5. Read the strongest candidate files, their direct dependencies, and relevant tests.
6. Broaden the search only when the evidence remains insufficient.

## Reread rules

Do not reread a file during the same execution unless:
- The file changed.
- A tool modified it.
- Validation requires its latest content.
- The user requests reanalysis.
- New evidence conflicts with the cached understanding.

## Search budget

- Begin with a small candidate set.
- Do not repeat an identical search without a new hypothesis.
- Do not inspect unrelated directories.
- Stop after identifying the implementation path and validation path.
- If focused discovery fails, state what remains unknown before broadening the search.

## Repository-wide scan triggers

A repository-wide scan is permitted only for:
- Explicit repository-wide architecture or impact analysis.
- Migration or modernization assessment.
- Agent taxonomy, inventory, or reorganization.
- Security or compliance audit.
- Broad dependency analysis.
- Focused discovery that demonstrably failed.

## Persistent index

`.ai/repository-index.md` is the durable map between sessions. Update it only when structure, key responsibilities, or validated commands change. Do not treat it as a cache of complete file contents.
