# Proposal: TUI Group Selection and Description Removal
**Status: Ready for Review**

## Intent
Item descriptions make each TUI row unnecessarily wide. Removing them gives
width back. Additionally, group headers are currently inert dividers; making
them selectable lets the user toggle an entire group in one keystroke.

## Scope
- **In scope**: removing the `description` field from `InstallItem` and all
  call sites; making group headers selectable (toggles all members of that group)
- **Out of scope**: adding descriptions back in any other form; changing item
  ids or groupings; `--list` output (drops the description column, id only)

## Delta

### MODIFIED
- `InstallItem`: `description` field removed
- TUI: group header entries become selectable; toggling a group header
  selects/deselects all items in that group (mirrors the parent/child toggle
  behaviour already in place)
- SPEC behaviour: group header toggling documented
- SPEC constraints: `description` field removed from `InstallItem` description;
  `--list` output updated to id-only

### REMOVED
- `description` field from `InstallItem` dataclass and all `InstallItem(...)`
  call sites
- `[dim]` description suffix from TUI item labels
- Description column from `--list` output
