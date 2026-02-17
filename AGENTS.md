# AGENTS Guidelines

- Read definitions and terminology in `DEFNS.md`
- Specifications live in `SPEC.md` files:
  - The **root** `SPEC.md` covers the project as a whole (structure, shared requirements, integration testing).
  - **Subfolder** `SPEC.md` files (e.g. `resources/tok/SPEC.md`) are scoped to that component — they own their own usage, implementation, and test definitions.
  - Subfolder specs inherit project-wide non-functional requirements (e.g. POS style from `DEFNS.md`) unless they explicitly override them.
  - When assessing drift or planning changes, read **all** `SPEC.md` files, not just the root.

## Change Management Process
All changes to `SPEC.md` files must follow this process:

### 1. Propose
Create a proposal in the `changes/` directory alongside the target `SPEC.md` (e.g. `changes/<change-name>/proposal.md` for the root spec, or `resources/tok/changes/<change-name>/proposal.md` for a subfolder spec).

```markdown
# <Change Name>

## Status (optional)
Draft | Ready

### Unresolved (optional, use with Draft)
- Items not yet fully specified

## Intent
Why this change is needed.

## Scope
- **In scope**: what this change covers
- **Out of scope**: what is deferred

## Delta

### ADDED
- New requirements being introduced

### MODIFIED
- Existing requirements being changed (note previous values)

### REMOVED
- Requirements being eliminated
```

Omit any empty delta sections (e.g. if nothing is removed, omit REMOVED).

### 2. Review
The proposal must be reviewed and approved before applying.

### 3. Apply
Apply the delta to the co-located `SPEC.md`. Pause between implementation steps and invite the operator to review. Do not modify any `SPEC.md` without an approved proposal.

### 4. Archive
Move the change folder to the co-located `changes/archive/YYYY-MM-DD-<change-name>/`.

## Coding Conventions
- Follow the POS standard defined in `DEFNS.md`

## Tests
- `test.sh` is the integration test for `bootstrap_inst.sh`/`install.py`. It launches a fresh incus container, runs setup, and verifies all tools, symlinks, and configs. Incus must be initialised on the host.
- Subfolders with their own `SPEC.md` may have local pytest tests (e.g. `resources/tok/test.py`). pytest must be the entry point (it discovers and runs `test_*` functions), so use `uv run --with pytest pytest <path> -v` to supply pytest as an ad-hoc dependency.
