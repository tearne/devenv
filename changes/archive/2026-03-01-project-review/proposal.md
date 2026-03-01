# Proposal: Project Review
**Status: Ready for Review**

## Intent
Carry out the review requested in `notes.md` and act on any actionable findings.

## Review Findings

**No action needed:**
- **Spec vs implementation:** Excellent alignment throughout. One negligible
  detail: the spec names biome architecture binaries as `biome-linux-x64` /
  `biome-linux-arm64`; the code derives these correctly at runtime. No change
  needed.
- **Split install.py:** At 821 lines with well-defined sections, splitting
  would add boilerplate without benefit. Single-file POS style is appropriate
  at this size.
- **POS style:** Working well. Subprocess used for shell commands; Python for
  control flow; lazy imports for `textual`/`rich`. No antipatterns.
- **Dead code:** None found. All imports, functions, and globals are used.
- **Nested tree representation:** Already added to SPEC.md in the
  hierarchical-groups change. No further action needed.

**Actionable findings:**

1. **Constraints section is verbose** — contains tool-specific implementation
   details (binary names, URLs, crate names, apt flags) that are already
   expressed in code. Could be condensed to architectural constraints only,
   with a short per-tool summary replacing the current wall of bullets.

2. **TUI selection logic has no unit tests** — `_collect_descendants`,
   `_collect_ancestors`, and the toggle handler are ~150 lines of core
   interaction logic with no coverage. These can be tested without launching
   the Textual app by calling the helper functions directly.

3. **`--all` flag not covered by unit tests** — `_parse_args` tests cover
   `--only`, `--skip`, `--list`, and unknown ids, but not `--all`.

4. **Minor installer inconsistency** — two git-config calls in `install_delta`
   and `install_difft` run unconditionally even when the tool is already
   installed and the function returns early. This is correct behaviour (config
   must be applied even if binary exists) but is not self-evident; a brief
   inline comment would clarify intent.

## Scope
- **In scope**: condensing the Constraints section of SPEC.md; adding unit
  tests for TUI helpers and `--all`; adding clarifying comments to
  `install_delta` and `install_difft`
- **Out of scope**: changes to install logic, TUI behaviour, or any
  functionality

## Delta

### MODIFIED
- `SPEC.md` Constraints: condensed to architectural constraints; per-tool
  install methods collapsed to a concise summary table or short prose
- `tests/unit.py`: new tests for `_collect_descendants`, `_collect_ancestors`,
  and `--all` flag
- `install.py`: inline comments on unconditional git-config calls in
  `install_delta` / `install_difft`
