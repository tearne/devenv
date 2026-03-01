# Design: Regroup Standalone Items
**Status: Ready for Review**

## Approach

Three `InstallItem` call sites in `_items()` gain or change a `group` argument.
No install logic, dependency, or ordering changes are needed.

```python
InstallItem("zellij", install_zellij, group="System", requires=["cargo-binstall"]),
InstallItem("delta",  install_delta,  group="Git",    requires=["cargo-binstall"]),
InstallItem("difft",  install_difft,  group="Git",    requires=["cargo-binstall"]),
```

The `# Standalone` comment above these items is removed.

## Tasks

1. Update the three `InstallItem` entries in `_items()` and remove the
   `# Standalone` comment
2. Update `SPEC.md`
3. Run unit tests (`uv run --with pytest pytest tests/unit.py`)
4. Confirm implementation complete and ready to archive
