# Proposal: Add JSON LSP for Helix
**Status: Ready for Review**

## Intent
Helix currently has no language server configured for JSON files. Adding a JSON LSP
provides formatting, linting, and hover documentation when editing JSON files (e.g.
`package.json`, config files).

`biome` is chosen over `vscode-json-language-server`: it is written in Rust, ships as
a single binary, and is installed via `cargo binstall` — the same mechanism already
used for `harper-ls`, `zellij`, `delta`, and `difft`. No Node.js dependency.

Helix 25.07.1 (current stable) does not include biome in its default language
configuration; `languages.toml` must be updated to register biome as the language
server for JSON and override the default `vscode-json-language-server` entry.

## Scope
- **In scope**: installing `biome` and updating `languages.toml` to use it for JSON
- **Out of scope**: using biome for JS/TS/CSS or other file types it supports; YAML,
  TOML, or other data-format LSPs

## Delta

### ADDED
- `biome` as a child of `helix` in the Helix group (`requires=["cargo-binstall"]`),
  installed via `cargo binstall --no-confirm biome`

### MODIFIED
- `resources/helix/languages.toml`: add `[[language]]` override for `json` pointing
  to `biome`, and a `[language-server.biome]` entry (`command = "biome"`,
  `args = ["lsp-proxy"]`)
- Tools Installed: Helix group gains `biome` as an LSP child
