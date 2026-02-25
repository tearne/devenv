# Proposal: Menu Item Improvements
**Status: Approved**

## Unresolved
- **Short name values**: the table below is a first suggestion — confirm or amend before
  this moves to design.

| Current id | Suggested short name |
|---|---|
| `htop` | `htop` |
| `btop` | `btop` |
| `unattended-upgrades` | `upgrades` |
| `incus` | `incus` |
| `rust` | `rust` |
| `zellij` | `zellij` |
| `helix` | `helix` |
| `harper-ls` | `harper` |
| `pyright` | `pyright` |
| `ruff` | `ruff` |
| `tok` | `tok` |

## Intent
Two small improvements to the installer menu:
1. The `unattended-upgrades` item silently changes behaviour beyond the name implies —
   it configures updates from all apt repositories, not just the default security-only
   scope. This should be visible to the user before they confirm.
2. Some item ids (e.g. `unattended-upgrades`, `harper-ls`) are awkward to type as CLI
   flag arguments. A short name for each item makes `--only`/`--skip` easier to use.

## Scope
- **In scope**: per-item description shown in the menu; short name aliases for CLI flags
- **Out of scope**: changes to installation behaviour; reordering of items

## Delta

### ADDED
- Each `InstallItem` gains an optional `description` field shown alongside its label in
  the menu (e.g. `unattended-upgrades` displays "updates all repos, not security-only").
- Each `InstallItem` gains a `short_name` field. Both the full `id` and `short_name` are
  accepted by `--only` and `--skip`.

### ADDED (continued)
- `-l`/`--list` flag: prints a plain-text table of all installable items (id, short
  name, description) and exits. Does not require a TTY.

### MODIFIED
- **Behaviour — Installation Process**: `--only`/`--skip` accept either the full item id
  or its short name.
- **Constraints**: item identifiers table updated to include short names.
