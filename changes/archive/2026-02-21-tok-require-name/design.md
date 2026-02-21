# Design: tok --add Requires Name

## Approach

All changes are confined to `resources/tok/tok.py`.

**Argument parsing** — `name` stays as `nargs="?"` (so `--list` needs no name), but its default becomes `None` and the help text is updated to drop the "default" reference.

**`--add` validation** — immediately after `parse_args()`, if `--add` is set and `name` is absent, print an error and exit. This gives a clear message rather than a cryptic failure later.

**`--add` flow** — the block that decides the name (lines 90–95: the `default.enc` existence check and the stdin prompt) is replaced by a single assignment from `args.name`.

**Retrieval flow** — `name = args.name or "default"` becomes `name = args.name`. If `name` is `None` (no argument given), print help and exit. The `if name == "default"` special-case in the "not found" error is removed — a missing secret always produces the same "not found" error regardless of name.

Tests are written first (TDD), targeting the existing test infrastructure implied by the spec's Verification section.

## Tasks

1. Write tests covering the changed behaviour:
   - `tok --add` with no name exits with an error
   - `tok --add <name>` stores without prompting for a name
   - `tok` with no arguments prints help and exits non-zero
   - `tok <name>` retrieves a named secret (existing round-trip test still passes)
2. Update `tok.py`: argument definition, `--add` validation, `--add` name assignment, retrieval fallback
3. Run tests to verify
