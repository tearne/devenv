# Proposal: tok --add Requires Name
**Status: Draft**

## Intent
The `-a`/`--add` flag currently defers asking for the secret name until after the secret and passphrase have been entered, and silently uses `"default"` as the name for the very first token. This makes scripted or muscle-memory use awkward and the "default" special-case adds unnecessary complexity. Requiring the name upfront as part of the command simplifies the UX and removes the special case entirely.

## Scope
- **In scope**: the `tok` script (`resources/tok/tok.py`) and its spec
- **Out of scope**: changes to how secrets are stored on disk, encryption, or clipboard behaviour

## Delta

### MODIFIED
- `tok --add` (and `-a`) now requires `name` to be supplied as a positional argument: `tok --add <name>`. The name is no longer prompted for during the add flow.
- Retrieval: `tok` with no `name` argument is no longer valid (no default token). `name` becomes a required positional argument for retrieval. `tok` with no arguments prints help.

### REMOVED
- Silent fallback to `"default"` as the token name when adding the first token.
- Interactive prompt for the token name during `--add`.
- The `default` token concept: there is no longer a specially-named default secret.
