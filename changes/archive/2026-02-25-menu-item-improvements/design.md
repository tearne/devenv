# Design: Menu Item Improvements
**Status: Approved**

## Approach

### InstallItem changes
Add two fields to the dataclass:

```python
short_name: str = ""      # defaults to id via __post_init__ if not supplied
description: str = ""     # shown in menu label and --list output
```

`__post_init__` sets `short_name = self.id` when the field is left empty, so items that
don't need an alias require no change at the call site.

Updated `_items()` registry (only differing values shown):

| id | short_name | description |
|----|-----------|-------------|
| `unattended-upgrades` | `upgrades` | updates all apt repos, not security-only |
| `harper-ls` | `harper` | |

All other items: `short_name` defaults to `id`, `description` left empty.

### `_parse_args()` changes

Build a `name_to_id` lookup covering both ids and short names:
```python
name_to_id = {item.id: item.id for item in items}
name_to_id |= {item.short_name: item.id for item in items}
```

`_validate()` checks supplied names against `name_to_id.keys()`. Names are resolved to
canonical ids before the set is returned, so the rest of the code is unaffected.

`-l`/`--list` added as a standalone flag (outside the `--all`/`--only`/`--skip` mutually
exclusive group). When present, print a plain-text table and exit 0 — no installation
occurs. The table columns are **id**, **short name**, **description**, with short name
omitted from the row when it equals the id (to reduce noise).

### Menu display
Descriptions are appended to the `SelectionList` label using Textual markup:

```
unattended-upgrades  [dim](updates all apt repos, not security-only)[/dim]
```

Items with no description are unaffected.

## Tasks

1. ~~Add `short_name` and `description` to `InstallItem` with `__post_init__`; update
   `_items()` with the new values~~
2. ~~Write unit tests: short name accepted by `--only`/`--skip`; full id still accepted;
   unknown name rejected; `--list` output contains id, short name, and description columns~~
3. ~~Update `_parse_args()`: `name_to_id` lookup, updated `_validate`, name→id resolution,
   `-l`/`--list` flag~~
4. ~~Update `run_selection_menu()` to append description markup to labels~~
5. ~~Run all unit tests (`uv run --with pytest pytest tests/unit.py`)~~
6. Confirm implementation complete and ready to archive
