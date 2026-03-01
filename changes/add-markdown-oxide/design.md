# Design: Add markdown-oxide
**Status: Ready for Review**

## Approach

### Installation
markdown-oxide is not published on crates.io, so `cargo binstall --no-confirm
markdown-oxide` would fail. Instead, use the `--git` flag:

```python
run("cargo binstall --no-confirm --git 'https://github.com/feel-ix-343/markdown-oxide' markdown-oxide")
```

This follows the same `cargo-binstall` pattern as `harper-ls` and others, so
`requires=["cargo-binstall"]` applies as usual.

### Item registration
Added to the Helix group after `harper-ls`:

```python
InstallItem("markdown-oxide", install_markdown_oxide, group="Helix", parent="helix", requires=["cargo-binstall"]),
```

### Helix config (`resources/helix/languages.toml`)
Add a language-server entry and append `markdown-oxide` to the markdown
language-servers list:

```toml
[language-server.markdown-oxide]
command = "markdown-oxide"

[[language]]
name = "markdown"
soft-wrap.enable = true
language-servers = ["marksman", "harper-ls", "markdown-oxide"]
```

### SPEC.md
- Helix group children list: add `markdown-oxide`
- Constraints: note `cargo binstall --git` as the install method

## Tasks

1. Add `install_markdown_oxide()` to `install.py`
2. Register the item in `all_items()` (after `harper-ls`)
3. Add language-server entry and update markdown language in `languages.toml`
4. Update `SPEC.md`
5. Confirm implementation complete and ready to archive
