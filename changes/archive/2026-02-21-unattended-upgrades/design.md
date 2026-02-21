# Design: Unattended Upgrades
**Status: Ready for Review**

## Approach

A new `install_unattended_upgrades()` function is added to `install.py`, called from `install()` alongside the other apt-installed tools. It does two things:

1. **Install the package** via apt, following the same pattern as `install_htop` etc.

2. **Write one config file** via `sudo tee`:
   - `/etc/apt/apt.conf.d/99unattended-upgrades-override` — sets `Allowed-Origins` to `"*:*"`, overriding the default `50unattended-upgrades` (which only covers security). The `99` prefix ensures it takes priority. The `20auto-upgrades` file (which enables the periodic timer) is created automatically by the package's postinst script and does not need to be written manually.

Writing via `sudo tee` fits naturally with the existing `run()`/`sudo()` infrastructure and handles all three execution modes (root, cached sudo, password sudo).

The code includes a comment explaining that `99unattended-upgrades-override` can be safely deleted to restore the default security-only behaviour, since it only overrides `Allowed-Origins` — the `50unattended-upgrades` file shipped with the package is left untouched.

No new unit tests — the config paths are system paths not easily redirectable, and the logic is a trivial fixed-content write. The integration test covers it.

## Tasks

- [ ] Add `install_unattended_upgrades()` to `install.py` and wire into `install()`, with explanatory comments on the config files
- [ ] Run existing unit tests to confirm no regressions
- [ ] Confirm implementation complete and ready to archive
