# Design: Fix Pyright LSP — Missing libatomic1 Dependency
**Status: Approved**

## Approach

`install_pyright()` in `install.py` gains a single `apt-get install libatomic1` call before the `uv tool install pyright` call. This follows the same `sudo()` pattern used elsewhere in the file. A comment explains the reason and links to the upstream Node.js issue.

No new tests are needed: the integration test already verifies that `pyright` is callable after installation, which would catch the failure mode this fixes.

## Tasks

- [x] Add `apt-get install -y -qq libatomic1` (with explanatory comment) to `install_pyright()` before the `uv tool install` call
- [x] Add `pyright --version` execution check to `tests/integration.sh` after the `command -v` loop
- [x] Confirm implementation complete and ready to archive
