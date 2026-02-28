# Proposal: Bugfix — Biome Install and difft Wrong Binary
**Status: Ready for Review**

## Intent

Two installer bugs:

1. **Biome install fails** — `cargo binstall --no-confirm biome` exits with code 86
   because biome's GitHub release assets (`biome-linux-x64`, `biome-linux-arm64`) do
   not follow the naming convention cargo-binstall auto-detects. Fix: switch to a
   direct download from GitHub releases (same approach as the helix installer).
   `requires=["cargo-binstall"]` is removed from the biome item as it is no longer
   needed.

2. **`git dft` prints "Hello, world!" instead of a diff** — `cargo binstall --no-confirm
   difft` installs a crate literally named `difft` on crates.io (a hello world
   program), not difftastic. The difftastic crate is named `difftastic`; it produces a
   binary called `difft`. Fix: change the install command from
   `cargo binstall --no-confirm difft` to `cargo binstall --no-confirm difftastic`.

   Note: the spurious `/root/.cargo/bin/difft` binary already on this system must be
   removed manually before re-running the installer, as `is_installed("difft")` would
   otherwise cause the install step to be skipped.

## Scope
- **In scope**: fixing the biome install method; fixing the difftastic crate name
- **Out of scope**: changing biome's role as JSON LSP; changing how difftastic is
  invoked from git

## Delta

### MODIFIED
- **`install_biome()`**: switch from `cargo binstall` to direct GitHub release
  download; binary placed in `~/.local/bin/` and made executable
- **`biome` item**: remove `requires=["cargo-binstall"]`
- **`install_difft()`**: `cargo binstall --no-confirm difft` →
  `cargo binstall --no-confirm difftastic`
- **Constraints** in SPEC: update biome install method; correct difftastic crate name
