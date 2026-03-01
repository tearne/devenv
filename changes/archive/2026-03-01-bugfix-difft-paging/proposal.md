# Proposal: Bugfix — git dft Not Paging with Colour
**Status: Ready for Review**

## Intent
`git dft` output is not paged, and when `less -R` is added as a pager it renders
in black and white. Two git config values are missing:

1. `difftastic.color = always` — difftastic detects it is not connected to a
   terminal (because it is invoked via `git difftool`) and suppresses colour
   output. This forces colour regardless.
2. `pager.difftool = true` — routes `git difftool` output through git's normal
   pager (the same path `git diff` uses). Git's default `less` invocation already
   includes `-R`, so ANSI colours render correctly.

## Scope
- **In scope**: adding both git config calls in `install_difft()`, applying them
  on the current system, and updating the spec.
- **Out of scope**: changing `core.pager` or any other pager configuration.

## Delta

### MODIFIED
- `install_difft()`: add `git config --global difftastic.color always` and
  `git config --global pager.difftool true`
- Constraints: add both values to the list of git config settings applied for
  `difft`
