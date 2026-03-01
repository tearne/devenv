# Design: Hierarchical Groups
**Status: Ready for Review**

## Approach

### Data model

```python
@dataclass
class Group:
    name: str
    parent: str | None = None  # group name or item id; None = top-level

@dataclass
class InstallItem:
    id: str
    installer: Callable
    parent: str | None = None  # group name or item id; None = top-level
    requires: list[str] = field(default_factory=list)
```

`parent` is the sole nesting field on both types. It can reference a group
name or an item id. `requires` carries install-order dependencies exclusively
(no longer derived from `parent`).

### `_groups()` registry

```python
def _groups() -> list[Group]:
    return [
        Group("System"),
        Group("Resource", parent="System"),
        Group("Rust"),
        Group("Git"),
        Group("Helix"),
    ]
```

### `_items()` — updated parent/requires assignments

```python
# System
InstallItem("htop",                install_htop,                parent="Resource"),
InstallItem("btop",                install_btop,                parent="Resource"),
InstallItem("unattended-upgrades", install_unattended_upgrades, parent="System"),
InstallItem("all-upgrades",        install_all_upgrades,        parent="unattended-upgrades", requires=["unattended-upgrades"]),
InstallItem("incus",               install_incus_and_init,      parent="System"),
InstallItem("tok",                 install_tok,                 parent="System"),
InstallItem("zellij",              install_zellij,              parent="System",  requires=["cargo-binstall"]),
# Rust
InstallItem("rust",                install_rust,                parent="Rust"),
InstallItem("rust-analyzer",       install_rust_analyzer,       parent="rust",    requires=["rust"]),
InstallItem("cargo-binstall",      install_cargo_binstall,      parent="rust",    requires=["rust"]),
# Git
InstallItem("delta",               install_delta,               parent="Git",     requires=["cargo-binstall"]),
InstallItem("difft",               install_difft,               parent="Git",     requires=["cargo-binstall"]),
# Helix
InstallItem("helix",               install_helix,               parent="Helix"),
InstallItem("biome",               install_biome,               parent="helix"),
InstallItem("harper-ls",           install_harper_ls,           parent="helix",   requires=["cargo-binstall"]),
InstallItem("pyright",             install_pyright,             parent="helix"),
InstallItem("ruff",                install_ruff,                parent="helix"),
```

This produces the following tree:

```
[System]
  [Resource]
    htop
    btop
  unattended-upgrades
    all-upgrades
  incus
  tok
  zellij
[Rust]
  rust
    rust-analyzer
    cargo-binstall
[Git]
  delta
  difft
[Helix]
  helix
    biome
    harper-ls
    pyright
    ruff
```

### `resolve_selection`

Remove `([item.parent] if item.parent else [])` from `requires_map`. All
install-order dependencies are now declared explicitly in `requires`.

### TUI rendering

Build a lookup of children for each node id (group names and item ids). Render
depth-first from root nodes (those with `parent=None`). Indent depth is the
node's depth in the tree × 2 spaces. Group header sentinel: `__group_{name}__`.

Toggle handler: when a group header is toggled, recursively collect all
descendant sentinels and item ids and select/deselect the entire subtree.
When an item with children is toggled, mirror state to its children (items
and group headers) recursively. When any node is toggled on, walk up the
tree ensuring each ancestor is selected.

### Unit tests

Update `parent`-based test fixtures to use the new field name and semantics.
Add tests covering: group header recursively toggles sub-group and its items;
item with children mirrors state downward; selecting a deeply nested item
selects all ancestors.

## Tasks

1. Add `Group` dataclass and `_groups()` registry; rename `InstallItem.group`
   → `parent` and remove old `parent` field (merging into one)
2. Update `_items()` with new `parent`/`requires` assignments
3. Update `resolve_selection` to drop `parent` from `requires_map`
4. Update TUI: tree build, depth-first render, recursive toggle
5. Update unit tests
6. Update `SPEC.md`
7. ~~Run unit tests (`uv run --with pytest pytest tests/unit.py`)~~
8. ~~Confirm implementation complete and ready to archive~~
