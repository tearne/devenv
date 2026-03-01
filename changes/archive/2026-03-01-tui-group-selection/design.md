# Design: TUI Group Selection and Description Removal
**Status: Approved**

## Approach

### 1. Remove descriptions
Remove the `description` field from `InstallItem` and all call sites. The two
items that currently have descriptions (`unattended-upgrades`, `all-upgrades`)
lose their dim suffix in the TUI label. `_print_item_list()` drops the
DESCRIPTION column and becomes an id-only list.

### 2. Group headers become selectable
Remove `disabled=True` from group header `Selection` entries. Set
`initial_state=True` to match the fully-selected default.

Update `on_selection_list_selection_toggled`: when the toggled value is a
`__group_<name>__` sentinel, select or deselect all items in that group (those
whose `item.group == name`) rather than returning early.

Group header state is write-only (used to drive children); it is not kept in
sync with child state. If individual children are toggled, the group header
reflects no particular state — it is a toggle-all action only.

### 3. SPEC updates
- Behaviour: group header toggling documented.
- Constraints: `description` removed from `InstallItem`; `--list` is id-only.

## Tasks

1. ~~Remove `description` from `InstallItem`, all `InstallItem(...)` call sites,
   and `_print_item_list()`~~
2. ~~Make group headers selectable and handle group-toggle in
   `on_selection_list_selection_toggled`~~
3. ~~Update `SPEC.md`~~
4. ~~Run unit tests (`uv run --with pytest pytest tests/unit.py`)~~
5. ~~Confirm implementation complete and ready to archive~~
