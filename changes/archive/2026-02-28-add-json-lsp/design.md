# Design: Add JSON LSP for Helix
**Status: Approved**

## Approach

Three small, independent changes:

1. **`install_biome()`** — follows the same pattern as other cargo-binstall installers
   (`install_harper_ls`, etc.): `is_installed` guard, `ensure_cargo_binstall()` safety
   net, `cargo binstall --no-confirm biome`.

2. **`_items()` registry** — add `biome` as a child of `helix` in the Helix group,
   mirroring `harper-ls`/`pyright`/`ruff`.

3. **`resources/helix/languages.toml`** — add a `[language-server.biome]` entry and a
   `[[language]]` override for `json` that points to it. The override replaces the
   Helix default (`vscode-json-language-server`) for JSON files. Follows the existing
   pattern in the file (harper-ls, pyright, ruff entries above).

No new unit tests are required: installer functions are not unit-tested (subprocess
calls), and config-file content is integration-test territory.

## Tasks

1. ~~Add `install_biome()` to `install.py`~~

2. ~~Add `biome` child item to `_items()`~~

3. ~~Add biome language server config and JSON language override to
   `resources/helix/languages.toml`~~

4. Run tests; confirm all pass
