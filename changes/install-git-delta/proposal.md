# Proposal: Install git-delta
**Status: Approved**

## Intent
`git-delta` (`delta`) provides syntax-highlighted, side-by-side-capable diffs as a
replacement for the default git pager. Integrating it into the installer makes it part
of the standard dev environment alongside the other tools.

## Scope
- **In scope**: installing `delta`; configuring it as the git pager
- **Out of scope**: delta theme/style customisation beyond defaults

## Delta

### ADDED
- `git-delta` (`delta`) installed via `cargo binstall git-delta`
- `delta` added to the selectable item registry with `rust` as a prerequisite
- Git configured to use `delta` as the core pager, with `[interactive]` diffFilter and
  `[delta]` section

### MODIFIED
- **Tools Installed**: `delta` added to the default selection set
- **Constraints**: git config written via `git config --global` at install time (keys:
  `core.pager`, `interactive.diffFilter`, `delta.navigate`); existing `~/.gitconfig`
  content is not touched beyond these keys
