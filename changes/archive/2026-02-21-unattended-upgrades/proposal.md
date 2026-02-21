# Proposal: Unattended Upgrades
**Status: Draft**

## Intent
The `unattended-upgrades` apt package should be installed and configured to automatically install updates from all pre-existing repositories as they become available. The default configuration only covers security updates; this change extends it to cover all origins already present on the system.

## Scope
- **In scope**: installing `unattended-upgrades` and writing its configuration in `install.py`
- **Out of scope**: adding new repositories; configuring automatic reboots or notifications

## Delta

### ADDED
- `unattended-upgrades` installed and configured as part of the setup process: automatically applies updates from all pre-existing repositories.

### MODIFIED
- Tools Installed: add `unattended-upgrades`.
