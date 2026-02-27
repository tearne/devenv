# Design: Install git-delta and difftastic
**Status: Approved**

## Approach

### New installer functions

**`install_delta()`** — installs the binary then applies git config unconditionally
(idempotent):
```python
def install_delta():
    with task("delta"):
        if is_installed("delta"):
            log("already installed, skipping")
        else:
            ensure_cargo_binstall()
            run("cargo binstall --no-confirm git-delta")
            log("done")
        run(r"""git config --global alias.dd '!f() { git diff "$@" | delta; }; f'""")
        run(r"""git config --global alias.dl '!f() { git log -p "$@" | delta; }; f'""")
```

**`install_difft()`**:
```python
def install_difft():
    with task("difftastic"):
        if is_installed("difft"):
            log("already installed, skipping")
        else:
            ensure_cargo_binstall()
            run("cargo binstall --no-confirm difft")
            log("done")
        run("""git config --global difftool.difftastic.cmd 'difft "$LOCAL" "$REMOTE"'""")
        run("git config --global difftool.prompt false")
        run("git config --global alias.dft 'difftool --tool=difftastic --no-prompt'")
```

Git config is applied on every run regardless of whether the binary was freshly
installed, making re-runs safe and self-healing.

### Registry entries
Added to `_items()` after `zellij`:
```python
InstallItem("delta", "delta",       install_delta, requires=["rust"]),
InstallItem("difft", "difftastic",  install_difft, requires=["rust"]),
```

`difft` uses `"difftastic"` as its label (the project name) and `"difft"` as its id
and default short name (the binary name).

## Tasks
1. ~~Add `install_delta()` and `install_difft()` installer functions~~
2. ~~Add `delta` and `difft` entries to `_items()`~~
3. Run unit tests (`uv run --with pytest pytest tests/unit.py`)
4. Confirm implementation complete and ready to archive
