# Proposal: Code Quality Improvements
**Status: Approved**

## Unresolved
- Of the two optional items below, which are in scope?

## Intent
Four improvements to `install.py`: two are now required by the updated POS spec, two
are optional quality improvements.

## Scope
- **In scope**: the two POS-required items (findings 3 and 4); whichever optional items
  are approved
- **Out of scope**: replacing the streaming subprocess output system; restructuring the
  logging/task indentation model

## Delta

### MODIFIED
- **`_print_item_list`** *(optional)*: replace manual column-width f-string arithmetic
  with `rich.table.Table`. `rich` is pre-approved and handles alignment and overflow
  more cleanly with less code.
- **`sudo` / `sudo_ok`** *(optional)*: extract a shared `_sudo_popen(cmd)` helper
  containing the three-branch privilege-escalation logic (root / passwordless sudo /
  password-piped sudo) that is currently duplicated across both functions.
- **Logfile lifecycle** *(POS required)*: replace explicit `_logfile.close()` at end of
  `main()` with `atexit.register(_logfile.close)` so the file is flushed and closed
  even when the script exits early via `sys.exit()`.
- **`open()` in `setup_local_bin_path`** *(POS required)*: replace `open(profile, "a")`
  with `profile.open("a")` for consistency with pathlib usage throughout the rest of
  the file.
