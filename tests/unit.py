"""Unit tests for install.py — file-operation logic only. No container required."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Satisfy the module-level guard before importing install
os.environ.setdefault("VIRTUAL_ENV", "1")

import pytest
import install


@pytest.fixture(autouse=True)
def reset_install_state(tmp_path, monkeypatch):
    """Redirect HOME to tmp_path and reset module globals before each test."""
    monkeypatch.setenv("HOME", str(tmp_path))
    install._warnings.clear()
    install._indent = 0


# ---------------------------------------------------------------------------
# _config_diff
# ---------------------------------------------------------------------------

def test_config_diff_equivalent(tmp_path):
    a = tmp_path / "a.toml"
    b = tmp_path / "b.toml"
    a.write_text("key = 'value'\n")
    b.write_text("key = 'value'  \n")  # trailing space — whitespace-equivalent
    assert install._config_diff(a, b) is None


def test_config_diff_different(tmp_path):
    a = tmp_path / "a.toml"
    b = tmp_path / "b.toml"
    a.write_text("key = 'value'\n")
    b.write_text("key = 'other'\n")
    assert install._config_diff(a, b) is not None


# ---------------------------------------------------------------------------
# _link_helix_config
# ---------------------------------------------------------------------------

def test_helix_config_creates_symlinks(tmp_path):
    install._link_helix_config()
    for filename in ("config.toml", "languages.toml"):
        dst = tmp_path / ".config" / "helix" / filename
        assert dst.is_symlink() and dst.exists()


def test_helix_config_skips_correct_symlink(tmp_path):
    install._link_helix_config()
    install._link_helix_config()  # second call — already correct
    assert len(install._warnings) == 0


def test_helix_config_replaces_dangling_symlink(tmp_path):
    dst = tmp_path / ".config" / "helix" / "config.toml"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.symlink_to("/nonexistent/path")
    assert not dst.exists()  # confirm dangling
    install._link_helix_config()
    assert dst.is_symlink() and dst.exists()


def test_helix_config_does_not_overwrite_different_real_file(tmp_path):
    dst = tmp_path / ".config" / "helix" / "config.toml"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("theme = 'catppuccin'\n")
    install._link_helix_config()
    assert dst.read_text() == "theme = 'catppuccin'\n"
    assert any("not overwriting" in msg for msg, _ in install._warnings)


def test_helix_config_skips_equivalent_real_file(tmp_path):
    src = install.SCRIPT_DIR / "resources" / "helix" / "config.toml"
    dst = tmp_path / ".config" / "helix" / "config.toml"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text())
    install._link_helix_config()
    assert not dst.is_symlink()  # left as a regular file
    assert len(install._warnings) == 0


# ---------------------------------------------------------------------------
# install_tok
# ---------------------------------------------------------------------------

def test_install_tok_creates_symlink(tmp_path):
    install.install_tok()
    dst = tmp_path / ".local" / "bin" / "tok"
    assert dst.is_symlink() and dst.exists()


def test_install_tok_skips_correct_symlink(tmp_path):
    install.install_tok()
    install.install_tok()  # second call — already correct
    assert len(install._warnings) == 0


def test_install_tok_replaces_dangling_symlink(tmp_path):
    dst = tmp_path / ".local" / "bin" / "tok"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.symlink_to("/nonexistent/tok")
    install.install_tok()
    assert dst.is_symlink() and dst.exists()


def test_install_tok_does_not_overwrite_real_file(tmp_path):
    dst = tmp_path / ".local" / "bin" / "tok"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("existing content")
    install.install_tok()
    assert dst.read_text() == "existing content"
    assert len(install._warnings) == 1


# ---------------------------------------------------------------------------
# setup_local_bin_path
# ---------------------------------------------------------------------------

def test_setup_local_bin_path_appends_to_profile(tmp_path):
    install.setup_local_bin_path()
    profile = tmp_path / ".profile"
    assert profile.exists()
    assert 'PATH="$HOME/.local/bin:$PATH"' in profile.read_text()


def test_setup_local_bin_path_skips_if_already_present(tmp_path):
    install.setup_local_bin_path()
    content_after_first = (tmp_path / ".profile").read_text()
    install.setup_local_bin_path()
    content_after_second = (tmp_path / ".profile").read_text()
    assert content_after_first == content_after_second
