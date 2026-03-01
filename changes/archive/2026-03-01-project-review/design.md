# Design: Project Review
**Status: Ready for Review**

## Approach

### 1. Condense SPEC.md Constraints

Replace the current per-tool bullets (lines 96–103) with concise prose. The
goal is to keep architectural constraints (language, runtime, approved deps,
file structure) while trimming tool-specific installation details that are
already expressed in code.

Proposed replacement (exact wording to be finalised during implementation):

```
- Python 3.12, `uv` as runtime. `textual` and `rich` as approved third-party
  dependencies. `uv` bootstrapped via `curl`.
- POS style (see `DEFINITIONS.md`).
- Installation methods by tool type:
  - apt (non-interactive): `htop`, `btop`, `incus`, `unattended-upgrades`
  - RustUp (via `curl`): `rust`; requires `build-essential`
  - `rustup component add`: `rust-analyzer`
  - `cargo binstall`: `cargo-binstall`, `zellij`, `git-delta`, `difftastic`,
    `harper-ls`; `markdown-oxide` uses `--git` (not on crates.io)
  - GitHub releases binary: `helix` (.deb), `biome` (arch-appropriate binary
    → `~/.local/bin/`)
  - `uv tool install`: `pyright` (also requires `libatomic1` apt),  `ruff`
- Git configured via `git config --global` for `delta` (`alias.dd`, `alias.dl`)
  and `difft` (`difftool.difftastic.cmd`, `difftool.prompt`, `alias.dft`,
  `difftastic.color`, `pager.difftool`). Aliases only; default behaviour
  unchanged. `difft` cmd uses `$HOME/.cargo/bin/difft` to avoid PATH issues in
  non-interactive shells.
- Root structure: [keep existing code block]
```

### 2. Extract TUI tree helpers for testability

`_collect_descendants` and `_collect_ancestors` are currently closures inside
`run_selection_menu`, closing over `children_of`, `parent_of`, and
`group_names`. Extract them as module-level functions with explicit parameters:

```python
def _collect_descendants(node_id: str, children_of: dict) -> list[str]:
    ...

def _collect_ancestors(node_id: str, parent_of: dict, group_names: set) -> list[str]:
    ...
```

The closures inside `run_selection_menu` are replaced with calls to these
functions, passing the locally-built data structures. No behaviour change.

### 3. New unit tests

**TUI helpers** — build a minimal `children_of` / `parent_of` / `group_names`
directly in the test (no need to construct `InstallItem`s):

- `_collect_descendants` of a leaf node returns `[]`
- `_collect_descendants` of a group includes direct children
- `_collect_descendants` recurses into sub-groups (deep tree)
- `_collect_ancestors` of a root node returns `[]`
- `_collect_ancestors` of a nested item returns all ancestors in order
  (immediate parent first)
- Ancestors of a group-type node return the group sentinel format

**`_parse_args` — `--all` flag:**
- `--all` returns all item ids

### 4. Inline comments on git config calls

In `install_delta` and `install_difft`, add a single comment above the git
config block explaining that config is applied unconditionally so it is set
correctly even on re-runs where the binary is already installed.

## Tasks

1. ~~Condense Constraints in `SPEC.md`~~
2. ~~Extract `_collect_descendants` and `_collect_ancestors` to module level~~
3. ~~Add unit tests for TUI helpers and `--all` flag~~
4. ~~Add inline comments to `install_delta` and `install_difft`~~
5. ~~Run unit tests (`uv run --with pytest pytest tests/unit.py`)~~
6. ~~Confirm implementation complete and ready to archive~~
