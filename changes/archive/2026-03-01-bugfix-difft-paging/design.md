# Design: Bugfix — git dft Not Paging with Colour
**Status: Ready for Review**

## Approach

Two `git config --global` calls added to `install_difft()` in `install.py`,
after the existing difftool config lines:

```python
run("git config --global difftastic.color always")
run("git config --global pager.difftool true")
```

Both values are also applied immediately on the current system via the same
commands run in the terminal.

No spec prose changes are needed beyond the constraints list.

## Tasks

1. ~~Add the two `git config` calls to `install_difft()` in `install.py`~~
2. ~~Apply both settings on the current system~~
3. ~~Update the constraints in `SPEC.md`~~
4. Archive
