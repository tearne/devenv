# Proposal: POS Spec Refinements
**Status: Note**

## Unresolved
- Whether and how to feed these back into the POS spec.

## Intent
Two patterns identified during the code quality review that generalise beyond this
script and could usefully be added to the POS spec:

1. **Prefer `Path.open()` over `open()`** — POS already recommends `pathlib`. A
   natural extension is to prefer `path.open(mode)` over `open(path, mode)` when a
   `Path` object is already in hand. This keeps pathlib usage consistent and avoids
   mixing idioms within the same file.

2. **Use `atexit` for resource cleanup** — when a script holds a long-lived resource
   (e.g. a log file opened at startup and closed at the end of `main()`), registering
   cleanup with `atexit` ensures the resource is released even if the script exits
   unexpectedly via `sys.exit()`. A short POS note along the lines of "use `atexit`
   for cleanup of resources that must be released even on unexpected exit" would
   generalise this pattern.
