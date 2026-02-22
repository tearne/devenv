# Design: Rust gcc Dependency
**Status: Ready for Review**

## Approach
Add a `sudo("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq build-essential")` call at the top of `install_rust()` in `install.py`, before the rustup invocation. This follows the same pattern already used in `install_pyright()` for `libatomic1`.

No changes to tests are needed — the integration test already verifies that `rustc` and `cargo` are callable after a full install run, which will implicitly exercise this fix.

## Tasks
- [x] Add `build-essential` apt install to `install_rust()` in `install.py`
- [x] Add a `rustc` compilation smoke test to `tests/integration.sh` (compile and run a minimal hello-world to verify the linker works)
- [ ] Confirm implementation complete and ready to archive
