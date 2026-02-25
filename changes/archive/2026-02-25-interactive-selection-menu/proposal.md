# Proposal: Interactive Selection Menu
**Status: Approved**

## Intent
Currently, customising which tools are installed requires editing `install.py` directly. A
full-screen interactive menu at startup would allow the user to select exactly what to
install before any work begins, making the installer accessible without needing to read
or modify source code.

## Scope
- **In scope**: a pre-install selection screen; dependency-driven activation of
  prerequisite items; grouping of Helix LSPs under a Helix parent entry;
  `--all`/`--only`/`--skip` flags for non-interactive invocation
- **Out of scope**: per-item configuration (e.g. choosing LSP dialect); persistent
  preference files

## Delta

### ADDED
- Before installation begins, a full-screen interactive menu is presented listing all
  installable items.
- Menu navigation supports arrow keys, `h`/`j`/`k`/`l`, and mouse.
- Spacebar or mouse click toggles selection of the focused item.
- All items are selected by default.
- LSPs (`harper-ls`, `pyright`, `ruff`, `vscode-json-language-server`) are listed as
  sub-items nested under a **Helix** group. Selecting or deselecting Helix toggles all
  its LSPs; selecting any LSP while Helix is deselected re-selects Helix automatically.
- Items with prerequisites that are themselves selectable (e.g. `harper-ls` requires
  `cargo`) activate those prerequisites automatically when selected, and deactivate them
  when no dependent item remains selected — unless the prerequisite was independently
  selected by the user. (`uv` is excluded from this logic as it is always installed.)
- Confirmation (Enter) proceeds to installation; `q` / Escape / `Ctrl-C` aborts.
- `--all` flag: skips the menu and installs everything.
- `--only <item> [<item> ...]` flag: skips the menu and installs only the named items.
- `--skip <item> [<item> ...]` flag: skips the menu and installs everything except the
  named items.
- The menu is implemented using the `textual` library (TUI framework for Python).

### MODIFIED
- **Behaviour — Installation Process**: removes "no further user input is required"
  (the menu precedes installation and requires interaction); adds that `--all`, `--only`,
  and `--skip` flags bypass the menu for non-interactive use; adds that when no flag is
  given and stdin is not a TTY, the script exits with an error directing the user to
  rerun with one of the three flags.
- **Constraints**: removes "No flags or configuration — to customise, edit `install.py`
  directly"; adds `textual` as an approved third-party dependency; adds documentation
  of item identifiers and their interdependencies.
- **Tools Installed**: list becomes the default selection set rather than a fixed list.
