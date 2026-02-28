# Design: Unattended-Upgrades Split
**Status: Approved**

## Approach

`install_unattended_upgrades()` currently does two things: installs the apt package and
writes `/etc/apt/apt.conf.d/99unattended-upgrades-override` to extend updates to all
repositories. Split into:

- `install_unattended_upgrades()` — installs the package only; removes the config-file
  step entirely
- `install_all_upgrades()` — writes the override file (the exact logic extracted from
  the current function)

A new `all-upgrades` child item is added to `_items()` with `parent="unattended-upgrades"`.
This proposal is applied after the rust-group restructuring of `_items()`, so
`all-upgrades` also carries `group="System"` at that point.

The `unattended-upgrades` description is updated to reflect its narrowed scope.

No unit tests currently exercise `install_unattended_upgrades()`. No test changes are
required unless a new test is added (not proposed here).

## Tasks

1. ~~Split `install_unattended_upgrades()`~~: remove the `override` config-file block
   from the existing function; extract it verbatim into a new `install_all_upgrades()`
   function wrapped in `with task("all-upgrades")`

2. ~~Update `_items()`~~: add `all-upgrades` child item (`parent="unattended-upgrades"`,
   `group="System"`, `description="extend automatic updates to all apt repositories"`);
   update `unattended-upgrades` description to `"automatic security updates (default)"`

3. Run tests; confirm all pass
