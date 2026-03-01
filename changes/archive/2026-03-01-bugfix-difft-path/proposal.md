# Proposal: Bugfix — difft Not Found in git difftool
**Status: Ready for Review**

## Intent
`git dft HEAD~1` fails with `difft: not found` because `git difftool` evaluates its
cmd via a non-interactive shell that does not source `~/.profile`, so `~/.cargo/bin`
is absent from PATH.

Fix: replace `difft` with `$HOME/.cargo/bin/difft` in the `difftool.difftastic.cmd`
config value. `$HOME` is present in the helper's environment and is expanded at eval
time, so the explicit path resolves correctly without hardcoding a user-specific
prefix at install time.

## Scope
- **In scope**: correcting the difftool cmd in `install_difft()`; updating the stored
  git config on this system
- **Out of scope**: `git dd`/`git dl` (delta runs via a `!`-alias which git invokes
  differently and already works)

## Delta

### MODIFIED
- `install_difft()`: `difft "$LOCAL" "$REMOTE"` →
  `$HOME/.cargo/bin/difft "$LOCAL" "$REMOTE"` in the `difftool.difftastic.cmd`
  git config call
