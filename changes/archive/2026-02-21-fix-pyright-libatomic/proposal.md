# Proposal: Fix Pyright LSP — Missing libatomic1 Dependency
**Status: Approved**

## Intent
`pyright-python` (installed via `uv`) downloads a prebuilt Node.js binary at runtime. Node.js 25+ requires `libatomic.so.1`, which is absent from minimal Ubuntu/Debian images (including Incus containers). This causes pyright to fail silently on startup, leaving the Python LSP non-functional in Helix. See: https://github.com/nodejs/node/issues/60790

## Scope
- **In scope**: installing `libatomic1` via apt before `pyright` in `install.py`
- **Out of scope**: changing how pyright itself is installed; pinning Node versions

## Delta

### MODIFIED
- `install_pyright()`: now installs `libatomic1` via apt before running `uv tool install pyright`
- Integration test: adds a `pyright --version` execution check after the `command -v` loop, to verify the Node.js runtime loads successfully (not just that the wrapper script is on PATH)
