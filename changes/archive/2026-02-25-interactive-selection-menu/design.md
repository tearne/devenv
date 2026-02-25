# Design: Interactive Selection Menu
**Status: Approved**

## Approach

### Item model
Introduce an `InstallItem` dataclass that captures everything the menu and installer need
to know about each installable item:

```python
@dataclass
class InstallItem:
    id: str                          # used by --only/--skip flags
    label: str                       # display name in menu
    installer: Callable              # function to call if selected
    parent: str | None = None        # parent item id (LSPs nest under "helix")
    requires: list[str] = ...        # prerequisite item ids (auto-activated)
```

The `ITEMS` list (defined near the top of the file, replacing the current `install()`
body) will be:

| id | label | parent | requires |
|----|-------|--------|----------|
| `htop` | htop | — | — |
| `btop` | btop | — | — |
| `unattended-upgrades` | unattended-upgrades | — | — |
| `incus` | incus | — | — |
| `rust` | Rust + Cargo + rust-analyzer | — | — |
| `zellij` | Zellij | — | `rust` |
| `helix` | Helix editor | — | — |
| `harper-ls` | harper-ls | `helix` | `rust` |
| `pyright` | pyright | `helix` | — |
| `ruff` | ruff | `helix` | — |
| `tok` | tok | — | — |

Notes:
- `uv` is excluded from the item registry — it is bootstrapped before `install.py` runs
  and is always present.
- `build-essential` is installed unconditionally inside `install_rust()` (as per the
  existing spec constraint) and is not a selectable item.
- `setup_local_bin_path()` always runs after the selected installers, regardless of
  selection.
- `init_incus()` is called inside a combined `install_incus_and_init()` helper when
  `incus` is selected, matching the current coupling in the code.

### Dependency auto-activation
`resolve_selection(selected: set[str], user_selected: set[str]) -> set[str]`:
- For each selected item, if it has `requires`, add those ids to `selected` (but not to
  `user_selected`).
- When an item is deselected in the TUI, remove it from `user_selected`; then recompute:
  remove any auto-selected prerequisite that is no longer required by any remaining
  selected item.
- In the starting state (all items selected by default), all items are in `user_selected`.

### Argument parsing
`argparse` with three mutually exclusive flags:

```
--all              install everything, skip menu
--only id [id …]   install only the listed items, skip menu
--skip id [id …]   install everything except the listed items, skip menu
```

If none of the three flags is given and `sys.stdin.isatty()` is `True`, launch the TUI.
If none is given and stdin is not a TTY, exit with an error directing the user to rerun
with `--all`, `--only`, or `--skip`.

### Textual TUI
A single-screen `textual` `App` using a `SelectionList` widget:

- All items listed as `Option(label, id)` entries; LSP sub-items indented with two
  leading spaces in their label.
- All items pre-selected.
- `j` / `↓` and `k` / `↑` move focus; `h` and `l` are aliased to `k` and `j`
  respectively (vim convention for a vertical list).
- `Space` toggles the focused item; mouse click on an item toggles it.
- Toggling the `helix` item also toggles all its LSP sub-items.
- Selecting any LSP sub-item while `helix` is unselected re-selects `helix`.
- Dependency auto-activation runs after every toggle.
- `Enter` closes the app and returns the selection.
- `q`, `Escape`, and `Ctrl-C` abort (exit the script).
- A footer bar shows key hints: `↑↓/jk navigate  space toggle  enter install  q quit`.

The app is extracted into a standalone function `run_selection_menu() -> set[str] | None`
that returns the selected IDs, or `None` if the user aborted.

### install() refactor
Replace the current no-argument `install()` with:

```python
def install(selected: set[str]):
    for item in ITEMS:
        if item.id in selected:
            item.installer()
    setup_local_bin_path()
```

### main() flow
```
parse args
→ if --all / --only / --skip: resolve selected set directly
→ else if TTY: selected = run_selection_menu(); abort if None
→ else: exit with error ("no TTY detected — rerun with --all, --only, or --skip")
→ init_password()
→ apt-get update
→ install(selected)
```

## Tasks

1. ~~Add `textual` to the `# /// script` dependencies block~~
2. ~~Define `InstallItem` dataclass and `ITEMS` registry; add combined
   `install_incus_and_init()` helper~~
3. ~~Implement `resolve_selection()` with dependency auto-activation logic~~
4. Write unit tests for `resolve_selection()` (prerequisite activation, deactivation,
   user-vs-auto-selected distinction, `--only`/`--skip` resolution)
5. ~~Implement `argparse` in `main()` and the non-interactive selection path~~
6. ~~Implement `run_selection_menu()` Textual app~~
7. ~~Refactor `install()` to accept `selected: set[str]` and wire into `main()`~~
8. ~~Run all unit tests (`uv run --with pytest pytest tests/unit.py`)~~
9. Confirm implementation complete and ready to archive
