# Design: Code Quality Improvements
**Status: Approved**

## Approach

### 1. `rich.table.Table` for `_print_item_list`
Add `rich` explicitly to the `# /// script` dependencies block (it is available
transitively via `textual`, but explicit is cleaner). Replace the manual column-width
arithmetic in `_print_item_list` with a `rich.table.Table`:

```python
from rich.console import Console
from rich.table import Table

def _print_item_list(items):
    table = Table(show_header=True)
    table.add_column("ID")
    table.add_column("SHORT NAME")
    table.add_column("DESCRIPTION")
    for item in items:
        sn = item.short_name if item.short_name != item.id else ""
        table.add_row(item.id, sn, item.description)
    Console().print(table)
```

### 2. Extract `_sudo_popen` helper
Both `sudo` and `sudo_ok` independently implement the three-branch privilege logic and
`Popen` construction. A shared helper extracts this:

```python
def _sudo_popen(cmd: str) -> subprocess.Popen:
    if os.geteuid() == 0:
        full = cmd
    elif _password is None:
        full = f"sudo {cmd}"
    else:
        full = f"sudo -S {cmd}"
    proc = subprocess.Popen(
        full, shell=True, text=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if _password is not None and os.geteuid() != 0:
        proc.stdin.write(_password + "\n")
    return proc
```

`sudo_ok` then becomes three lines. `sudo` continues to delegate to `run()` for the
root/passwordless cases (preserving their logging), and uses `_sudo_popen` only in the
password branch.

### 3. `atexit` for logfile + `Path.open()`
Add `atexit` to the stdlib imports. In `main()`:
- Open the logfile with `(SCRIPT_DIR / "install.log").open("w")` (pathlib idiom)
- Register close with `atexit.register(_logfile.close)` immediately after opening
- Remove the explicit `_logfile.close()` at the end of `main()`

### 4. `profile.open("a")` in `setup_local_bin_path`
One-line change: `open(profile, "a")` → `profile.open("a")`.

## Tasks
1. ~~Add `rich` to `# /// script` dependencies; rewrite `_print_item_list` with
   `rich.table.Table`~~
2. ~~Extract `_sudo_popen`; simplify `sudo_ok` and `sudo` to use it~~
3. ~~Add `atexit` import; use `atexit.register` for logfile; use `Path.open()` for
   logfile open~~
4. ~~Replace `open(profile, "a")` with `profile.open("a")` in `setup_local_bin_path`~~
5. Run unit tests (`uv run --with pytest pytest tests/unit.py`)
6. Confirm implementation complete and ready to archive
