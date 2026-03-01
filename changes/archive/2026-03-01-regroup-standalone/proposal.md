# Proposal: Regroup Standalone Items
**Status: Ready for Review**

## Intent
`zellij`, `delta`, and `difft` are currently ungrouped ("Standalone"), leaving
them without a visual header in the TUI. Grouping them makes the menu cleaner
and better reflects their character: `delta` and `difft` are git tools;
`zellij` is a terminal multiplexer closer in nature to `htop`/`btop`.

## Scope
- **In scope**: assigning `group` values to `zellij`, `delta`, and `difft`;
  updating SPEC accordingly
- **Out of scope**: changing install logic, dependencies, or any other items

## Delta

### ADDED
- New `Git` group containing `delta` and `difft`

### MODIFIED
- `zellij`: moved into the `System` group (no `parent`; `requires` unchanged)
- `delta`: assigned `group="Git"` (previously ungrouped)
- `difft`: assigned `group="Git"` (previously ungrouped)
- SPEC Tools Installed: `zellij` listed under System group; `delta` and `difft`
  listed under new Git group
