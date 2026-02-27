# Proposal: Install git-delta and difftastic
**Status: Approved**

## Unresolved
- ~~How much git configuration should be applied at install time?~~ **Resolved: Option B selected.**

### Option A: Install only, no git config
Both binaries land on PATH. Default git behaviour is completely untouched.

**What is done**: `cargo binstall git-delta` and `cargo binstall difft`. No
`git config --global` calls.

**Usage in practice**:
```sh
git diff | delta                        # pipe any diff through delta manually
git diff HEAD~1 | delta
git log -p | delta

GIT_EXTERNAL_DIFF=difft git diff        # run a single diff through difftastic
GIT_EXTERNAL_DIFF=difft git show HEAD
```

---

### Option B: Aliases only, no defaults changed ✓ SELECTED
Both tools exposed via git aliases. `git diff`, `git log`, `git show` etc. all behave
exactly as before. The aliases are the only addition.

Aliases use a shell function pattern (`!f() { ...; }; f`) so that arguments are
forwarded correctly — e.g. `git dd HEAD~1` or `git dd -- src/main.py` work as expected.

**Alias names chosen: `git dd`, `git dl`, `git dft`.**

**What is done**: five `git config --global` calls:
```sh
git config --global alias.dd  '!f() { git diff "$@" | delta; }; f'
git config --global alias.dl  '!f() { git log -p "$@" | delta; }; f'
git config --global difftool.difftastic.cmd 'difft "$LOCAL" "$REMOTE"'
git config --global difftool.prompt false
git config --global alias.dft 'difftool --tool=difftastic --no-prompt'
```

**Usage in practice**:
```sh
git dd                    # diff working tree via delta
git dd HEAD~1             # diff a specific commit via delta
git dd -- src/main.py     # diff a specific file via delta
git dl                    # log -p via delta
git dl --since=yesterday  # log -p filtered, via delta

git dft                   # diff all changed files via difftastic
git dft -- src/main.py    # diff a specific file via difftastic
```

---

### Option C: difftool config for difftastic, nothing for delta
Difftastic is wired as a named difftool and exposed via `git dft` (it genuinely
requires this setup to work as a git difftool). Delta is installed as a binary only,
with no git config — used by piping manually.

**What is done**: two `git config --global` calls:
```sh
git config --global difftool.difftastic.cmd 'difft "$LOCAL" "$REMOTE"'
git config --global alias.dft 'difftool --tool=difftastic --no-prompt'
```

**Usage in practice**:
```sh
git diff | delta        # delta used manually by piping

git dft                 # difftastic via alias
git dft -- path/to/file
```

---

## Intent
Two complementary diff tools for git:
- `git-delta` (`delta`) — a syntax-highlighted pager for git diff output.
- `difftastic` (`difft`) — a structural diff tool that understands syntax via
  tree-sitter, useful when a semantically-aware diff is more informative than a
  line-based one.

## Scope
- **In scope**: installing `delta` and `difft`; git configuration per chosen option
- **Out of scope**: delta theme/style customisation beyond defaults; difftastic language
  configuration

## Delta

### ADDED
- `git-delta` (`delta`) installed via `cargo binstall git-delta`; added to the selectable
  item registry with `rust` as a prerequisite
- `difftastic` (`difft`) installed via `cargo binstall difft`; added to the selectable
  item registry with `rust` as a prerequisite
- Git configured via `git config --global` at install time (Option B — aliases only):
  - `alias.dd` — `git diff` piped through delta, with argument forwarding
  - `alias.dl` — `git log -p` piped through delta, with argument forwarding
  - `difftool.difftastic.cmd` — wires `difft` as a named difftool
  - `difftool.prompt` — set to false
  - `alias.dft` — `git difftool --tool=difftastic --no-prompt`

### MODIFIED
- **Tools Installed**: `delta` and `difft` added to the default selection set
- **Constraints**: git config keys written at install time documented (`alias.dd`,
  `alias.dl`, `difftool.difftastic.cmd`, `difftool.prompt`, `alias.dft`); existing
  `~/.gitconfig` content is not touched beyond these keys
