# Proposal: Rust Group, System Group, and Short-Name Removal
**Status: Ready for Review**

## Intent
Four related changes:
1. **Label fix**: remove "Cargo" from the label "Rust + Cargo + rust-analyzer" — Cargo
   is bundled automatically by rustup and is not a separately installed component.
2. **Group model**: add a `group: str | None` field to `InstallItem` for purely visual
   section headers. `group` is independent of `parent`:
   - `parent` = install-level relationship (cascading toggles, `requires` resolution)
   - `group` = visual-only section label (non-toggleable TUI header)
3. **Rust group and System group**: apply the group model to introduce two new groups.
4. **Short-name removal**: remove the `short_name` field. Short names were motivated
   largely by `harper` as an alias for `harper-ls`, but with the group model making the
   hierarchy explicit this no longer feels necessary. Items are always referred to by
   their full id.

## Proposed item hierarchy

Legend: `[G]` = group header (non-installable); `←` = installable group parent; `→` = child

```
[G] System
      htop
      btop
      unattended-upgrades
      incus
      tok

[G] Rust
      rust              ←    installs rustup/rustc/cargo
        rust-analyzer   →    rustup component add rust-analyzer
        cargo-binstall  →    required by zellij, delta, difft, harper-ls

    zellij                   [requires: cargo-binstall]
    delta                    [requires: cargo-binstall]
    difft                    [requires: cargo-binstall]

[G] Helix
      helix             ←    installs hx + config symlinks
        harper-ls       →    [requires: cargo-binstall]
        pyright         →
        ruff            →
```

Cross-group `requires` links (resolved at confirmation time, not real-time):
- `zellij`, `delta`, `difft` → `cargo-binstall`
- `harper-ls` → `cargo-binstall`
- `cargo-binstall` → `rust` (parent, so selecting cargo-binstall selects rust group)

## Scope
- **In scope**: `group` field on `InstallItem`; label correction; Rust group (rust,
  rust-analyzer, cargo-binstall); System group (htop, btop, unattended-upgrades, incus,
  tok); Helix group adopts `group` field for consistency; updated `requires`
  relationships; deferred cross-group dependency resolution with confirmation summary;
  short-name removal
- **Out of scope**: changing the rustup installation mechanism; adding new Rust
  toolchain components; grouping zellij/delta/difft (they remain ungrouped)

## Delta

### ADDED
- `group: str | None` field on `InstallItem` — visual-only section label; TUI renders
  items sharing a `group` value under a non-toggleable header
- Rust group: `rust` as parent (installs rustup/rustc/cargo); `rust-analyzer` and
  `cargo-binstall` as optional children (selected by default)
- System group: `htop`, `btop`, `unattended-upgrades`, `incus`, `tok` all carry
  `group="System"` with no shared parent
- After the user confirms in the TUI (Enter), cross-group dependency resolution runs;
  if any items were added, a summary is shown and the user is prompted to confirm
  before installation begins
- For non-menu invocations, auto-resolved cross-group dependencies emit a warning to
  stdout and the log identifying which items were added

### MODIFIED
- **Label**: "Rust + Cargo + rust-analyzer" → "Rust" (Cargo is implicit in rustup;
  `rust-analyzer` becomes a child item)
- **TUI behaviour**: within-group parent/child toggling remains real-time; cross-group
  dependency resolution is deferred to confirmation time
- **Downstream `requires`**: `zellij`, `harper-ls`, `delta`, `difft` change from
  `requires=["rust"]` to `requires=["cargo-binstall"]`; `cargo-binstall` carries
  `requires=["rust"]`, preserving the transitive chain
- **Helix group**: helix and its children gain `group="Helix"` for consistency (no
  behavioural change)
- **Tools Installed**: updated to reflect group structure and removal of short names

### REMOVED
- `short_name` field from `InstallItem` (and its `__post_init__` defaulting logic)
- Short-name support in `--only`/`--skip` (flags now accept full ids only)
- Short-name column from `--list` output
- `(short: upgrades)` and `(short: harper)` from all documentation
