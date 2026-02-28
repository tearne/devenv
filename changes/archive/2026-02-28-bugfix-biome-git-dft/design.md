# Design: Bugfix — Biome Install and difft Wrong Binary
**Status: Approved**

## Approach

### Biome
Replace `install_biome()` with a direct GitHub release download, following the same
pattern as `install_helix()`. Architecture is detected via `platform.machine()`
(`aarch64` → `arm64`, everything else → `x64`). The binary is placed in
`~/.local/bin/` (already on PATH via `setup_local_bin_path()`). `platform` is added
to the imports. `requires=["cargo-binstall"]` is removed from the biome item.

### difft
Single-word fix: `cargo binstall --no-confirm difft` →
`cargo binstall --no-confirm difftastic`.

## Tasks

1. ~~Add `import platform`; replace `install_biome()` with direct GitHub download;
   remove `requires=["cargo-binstall"]` from biome item~~

2. ~~Fix `install_difft()`: `difft` → `difftastic` in the binstall command~~

3. Run tests; confirm all pass
