# Proposal: Unattended-Upgrades Split
**Status: Ready for Review**

## Intent

Currently `unattended-upgrades` installs the package *and* writes configuration to
extend automatic updates to all apt repositories (not just security). This conflates
installation with a policy decision that some users may not want.

Split into two items:
- **`unattended-upgrades`** (parent): installs the package with its default behaviour —
  automatic security updates only.
- **child item** (name TBD): applies the configuration that extends updates to all apt
  repositories. Selected by default so existing behaviour is preserved for users who
  do not customise the menu.

## Proposed item hierarchy (within System group)

```
[G] System
      htop
      btop
      unattended-upgrades          ← installs package; default: security updates only
        all-upgrades               → configures to update all apt repositories
      incus
      tok
```

## Scope
- **In scope**: splitting install from configuration; adding the child item; updating
  the item description to reflect the narrower default behaviour
- **Out of scope**: changing which apt configuration file is written; changing the
  update schedule or other unattended-upgrades settings

## Delta

### ADDED
- `all-upgrades` child under `unattended-upgrades`: applies configuration to extend
  automatic updates to all apt repositories; selected by default

### MODIFIED
- **`unattended-upgrades` installer**: stripped of the all-repos configuration step;
  now installs the package only (default behaviour: security updates)
- **`unattended-upgrades` description**: updated to reflect security-only default
  (previously noted "updates all apt repos, not security-only")
- **Tools Installed** in SPEC: updated to reflect the split
