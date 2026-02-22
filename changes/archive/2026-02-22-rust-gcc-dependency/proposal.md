# Proposal: Rust gcc Dependency
**Status: Ready for Review**

## Intent
`install_rust()` installs Rust via rustup but does not first install `build-essential`. Rustup requires a C linker and C standard library headers to link Rust binaries. On a minimal Ubuntu/Debian image these are absent, causing Rust compilation to fail.

## Scope
- **In scope**: installing `build-essential` as a prerequisite in `install_rust()`
- **Out of scope**: any other dependency changes

## Delta

### MODIFIED
- `install_rust()` must install `build-essential` (apt) before invoking rustup
