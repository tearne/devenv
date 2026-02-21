# Proposal: Isolated Test Environment
**Status: Draft**

## Intent
The integration test (`test.sh`) requires nested container support on the host, which is often unavailable or slow, creating friction for routine development. The intent is to introduce a lightweight unit test layer that can run without containers, covering the parts of `install.py` logic that don't require actual tool installation. The existing `test.sh` is retained for full integration testing when containers are available.

## Scope
- **In scope**: a unit test module at the project root; spec update to describe the two test layers
- **Out of scope**: replacing or modifying `test.sh`; mocking tool installation steps (apt, cargo, curl, etc.)

## Delta

### ADDED
- Unit tests for `install.py` runnable without a container.

### MODIFIED
- Verification section: describes two test layers — unit tests (no container needed) and the existing integration test (container required).
