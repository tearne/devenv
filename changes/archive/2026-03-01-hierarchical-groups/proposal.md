# Proposal: Hierarchical Groups
**Status: Ready for Review**

## Intent
The current `group` field on `InstallItem` is a flat string label — groups are
visual dividers only. The `parent` field provides one level of item-under-item
nesting, but cannot nest a group under an item or a group under another group.
This change introduces a unified tree: groups are first-class nodes, and any
node (group or item) can be the parent of any other node. Groups display as
`[Name]` and recursively toggle all descendants. Items can still be nested
directly under other items when a dependency relationship warrants it (e.g.
`all-upgrades` under `unattended-upgrades`; `rust-analyzer` under `rust`).
Sub-groups can themselves be nested under items (e.g. a `[BC]` group under A).

This also enables the `[Resource]` sub-group (htop, btop) within System.

## Scope
- **In scope**: new `Group` dataclass; unified `parent` reference on both
  `Group` and `InstallItem` (can point to a group name or an item id);
  recursive toggle in the TUI; making `requires` fully explicit (no longer
  derived from `parent`); introducing `[Resource]` sub-group; updating SPEC
- **Out of scope**: changes to install logic beyond migrating implicit
  `parent`-driven dependencies to `requires`; changing which items exist or
  how they are installed

## Delta

### ADDED
- `Group` dataclass with `name` and `parent: str | None` (parent can be a
  group name or an item id)
- `_groups()` registry
- `[Resource]` sub-group under System, containing `htop` and `btop`
- TUI: recursive group toggle (selecting/deselecting a group header affects all
  descendant groups and items)
- TUI: group headers displayed with `[Name]` square-bracket notation at
  appropriate indent depth

### MODIFIED
- `InstallItem.group` (flat string) replaced by `InstallItem.parent: str | None`
  pointing to either a group name or an item id (unified parent reference)
- `rust-analyzer` and `cargo-binstall`: install dependency on `rust` made
  explicit via `requires=["rust"]` (previously implicit through `parent`)
- `resolve_selection`: `requires_map` no longer derives deps from `parent`;
  `requires` is now the sole source
- SPEC: item model, TUI behaviour, and group listing updated throughout

### REMOVED
- `InstallItem.group` flat string field (replaced by `parent`)
- Existing single-level parent/child toggle logic (superseded by recursive
  group/item toggle)
