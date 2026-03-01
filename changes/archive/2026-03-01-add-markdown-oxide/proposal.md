# Proposal: Add markdown-oxide
**Status: Ready for Review**

## Intent
Add [markdown-oxide](https://github.com/Feel-ix-343/markdown-oxide), a PKM-focused
Markdown language server, as an optional Helix child item. It provides completions,
references, and backlink navigation for Markdown files.

## Scope
- **In scope**: installing the `markdown-oxide` binary; replacing `marksman` with
  `markdown-oxide` in `languages.toml`; adding it as a selectable item (child of
  `helix`)
- **Out of scope**: any markdown-oxide workspace/settings configuration beyond
  registering it with Helix

## Delta

### ADDED
- New installable item `markdown-oxide` (child of `helix`, requires `cargo-binstall`)
  installed via `cargo binstall --git 'https://github.com/feel-ix-343/markdown-oxide'
  markdown-oxide` (not published on crates.io; F#/.NET runtime would be required
  for marksman, making markdown-oxide the cleaner replacement)
- `[language-server.markdown-oxide]` entry in `resources/helix/languages.toml`

### MODIFIED
- `languages.toml` markdown `language-servers`: `["marksman", "harper-ls"]` →
  `["markdown-oxide", "harper-ls"]`
- Helix group: `markdown-oxide` listed as an optional child alongside `biome`,
  `harper-ls`, `pyright`, `ruff`
- Constraints: `markdown-oxide` added to the list of Helix child items and their
  install methods

### REMOVED
- `marksman` from the markdown `language-servers` list (was never installed by this
  script; covered by markdown-oxide without additional runtime dependencies)
