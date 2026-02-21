# Design: Isolated Test Environment

## Approach

`install.py` contains two clearly separable concerns: tool installation (apt, cargo, curl — not testable without a real system) and file operations (symlink creation, config diffing, PATH setup — fully testable with a temp directory). The unit tests target only the latter.

**Importing `install.py`**: the module-level `VIRTUAL_ENV` guard passes when pytest runs under uv. Tests set `HOME` to `tmp_path` so all `Path.home()` calls resolve into the temp directory. `install.SCRIPT_DIR` resolves to the real project root at import time, giving tests access to the real resource files.

**State isolation**: `install._warnings` and `install._indent` are module-level globals. A pytest fixture resets them before each test.

**Functions under test**:
- `_link_helix_config()` — symlink creation, dangling-symlink replacement, config-not-overwritten, whitespace-equivalent skip
- `install_tok()` — same symlink logic for `tok`
- `setup_local_bin_path()` — appends PATH export to `.profile`; skips if already present
- `_config_diff()` — returns `None` for whitespace-equivalent files, a diff string otherwise

## Tasks

1. Write `test.py` at the project root covering the scenarios above
2. Run tests to verify
3. Update `SPEC.md`
