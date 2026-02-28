# Design: Rust Group, System Group, and Short-Name Removal
**Status: Approved**

## Approach

### Short-name removal
Remove `short_name` and `__post_init__` from `InstallItem`. In `_parse_args`, simplify
`name_to_id` to a plain `{item.id: item.id}` dict. Drop the "SHORT NAME" column from
`_print_item_list`.

### `group` field
Add `group: str | None = None` to `InstallItem` — purely visual; no install logic
depends on it. Group headers are rendered in the TUI as disabled `Selection` entries
(value prefix `__group_`), which Textual shows as non-interactive. They are filtered
out of the result in `action_confirm`. Items in a group receive one extra level of
indent; children of an installable parent receive two.

### `resolve_selection` — parent as implicit require
`resolve_selection` currently uses only `requires`. With `parent`-linked children
(rust-analyzer, cargo-binstall), CLI paths such as `--only rust-analyzer` must also
pull in the parent. Update `resolve_selection` to treat `parent` as an implicit require
alongside the explicit `requires` list.

### Item registry
- `rust` label → "Rust"; gains `group="Rust"`
- `rust-analyzer` split out as a child: `parent="rust"`, `group="Rust"`, installed via
  `rustup component add rust-analyzer` (runs after `install_rust()` so `rustup` is on
  PATH)
- `cargo-binstall` added as a child: `parent="rust"`, `group="Rust"`, installed via the
  existing `ensure_cargo_binstall()` logic (renamed `install_cargo_binstall()`)
- `zellij`, `delta`, `difft`, `harper-ls` `requires` changed from `["rust"]` to
  `["cargo-binstall"]`
- System group: `htop`, `btop`, `unattended-upgrades`, `incus`, `tok` gain
  `group="System"`; no shared parent
- Helix group: `helix`, `harper-ls`, `pyright`, `ruff` gain `group="Helix"` for
  consistency (no behavioural change)
- `ensure_cargo_binstall()` guard calls inside individual installers (`install_zellij`,
  etc.) are retained as defensive safety nets

### TUI changes
Remove the `resolve_selection` block from `on_selection_list_selection_toggled` — cross-
group prerequisite activation is no longer real-time. Retain the existing parent/child
mirroring logic unchanged.

### Confirmation step
After `run_selection_menu` returns (TUI path only), call `resolve_selection` and compare
with the widget result. If items were added, print an apt-style summary (one `+` line
per added item) and prompt `Continue? [Y/n]`. Abort on "n". For CLI flag paths
(`--all`/`--only`/`--skip`), emit a `warn()` per auto-added item instead of prompting.

## Tasks

1. ✓ Update unit tests
   - Remove: `test_short_name_defaults_to_id`, `test_short_name_explicit`,
     `test_parse_args_only_accepts_short_name`, `test_parse_args_skip_resolves_short_name`
   - Update: `_named_items()` helper (drop `short_name=`); `test_parse_args_list_output`
     (remove "short" assertion); `test_parse_args_list_shows_description` (drop
     `short_name=` kwarg)
   - Add: `test_group_defaults_to_none`; `test_resolve_child_implicitly_requires_parent`
     (child with `parent` but no explicit `requires` pulls in the parent)

2. ✓ Remove `short_name` from `InstallItem`: remove field and `__post_init__`; simplify
   `_parse_args` `name_to_id` to id-only; remove "SHORT NAME" column from
   `_print_item_list`

3. ✓ Add `group: str | None = None` to `InstallItem`

4. ✓ Update `resolve_selection`: build the requires map as
   `item.requires + ([item.parent] if item.parent else [])`

5. ✓ Update `_items()` registry: apply groups; split `rust-analyzer` and
   `cargo-binstall` into separate child items; update `requires` on dependents;
   update rust label; add tok to System group

6. ✓ Add `install_rust_analyzer()` and `install_cargo_binstall()`; update
   `install_rust()` to remove the rust-analyzer step

7. ✓ TUI: group headers and cross-group deactivation
   - `_make_selections()`: insert a disabled `Selection(f"[bold]{g}[/bold]",
     f"__group_{g}__", disabled=True)` when `item.group` changes; update indentation
     (`"  "` for group member, `"    "` for group child)
   - `on_selection_list_selection_toggled`: add early return for `__group_` values;
     remove the `resolve_selection` auto-activation block
   - `action_confirm`: filter `__group_` values from `sl.selected` before storing result

8. ✓ `main()` confirmation/warning step: after TUI returns, resolve and diff; print
   `+`-prefixed summary and prompt if additions exist; for CLI paths emit `warn()` per
   addition

9. ✓ Run tests; confirm all pass
