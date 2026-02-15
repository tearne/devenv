"""Tests for tok.py — pytest rewrite of test_tok.sh."""

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

TOK = str(Path(__file__).parent / "tok.py")


def run_tok(args, stdin_text="", tok_dir=None, env_extra=None):
    env = os.environ.copy()
    if tok_dir:
        env["TOK_DIR"] = str(tok_dir)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [TOK, *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
    )


def add_secret(tok_dir, secret, passphrase, name=None):
    """Add a secret. If name is given it's appended (for the second+ secret)."""
    stdin = f"{secret}\n{passphrase}\n{passphrase}\n"
    if name is not None:
        stdin += f"{name}\n"
    return run_tok(["--add"], stdin_text=stdin, tok_dir=tok_dir)


# ---- Tests ----


def test_encrypt_decrypt_roundtrip(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "my-secret-token"


def test_named_secret_roundtrip(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--stdout", "work"], stdin_text="testpass2\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "another-secret"


def test_default_still_works_after_named(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--stdout"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode == 0
    assert r.stdout.strip() == "my-secret-token"


def test_list_includes_default(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--list"], tok_dir=tmp_path)
    assert "default" in r.stdout


def test_list_includes_named(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    add_secret(tmp_path, "another-secret", "testpass2", name="work")
    r = run_tok(["--list"], tok_dir=tmp_path)
    assert "work" in r.stdout


def test_wrong_passphrase_rejected(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout"], stdin_text="wrongpass\n", tok_dir=tmp_path)
    assert r.returncode != 0


def test_missing_secret_rejected(tmp_path):
    add_secret(tmp_path, "my-secret-token", "testpass")
    r = run_tok(["--stdout", "nonexistent"], stdin_text="testpass\n", tok_dir=tmp_path)
    assert r.returncode != 0


def test_signal_clears_clipboard(tmp_path):
    """Verify that SIGTERM during the clipboard-clear wait triggers an immediate clear.

    We create a fake /dev/tty (a FIFO) so OSC 52 writes go to a file we can inspect,
    then send SIGTERM and confirm the clear sequence appears.
    """
    import base64

    add_secret(tmp_path, "my-secret-token", "testpass")

    fake_tty = tmp_path / "fake_tty"
    osc_log = tmp_path / "osc_log"

    # A helper script that opens the FIFO as /dev/tty via _open_tty monkeypatch,
    # by overriding _open_tty in tok before main() runs.
    wrapper = tmp_path / "wrapper.py"
    wrapper.write_text(f"""\
import sys, os
sys.path.insert(0, os.path.dirname({TOK!r}))
os.environ["TOK_DIR"] = {str(tmp_path)!r}

import tok
tok._open_tty = lambda: open({str(osc_log)!r}, "a")
tok.main()
""")

    env = os.environ.copy()
    env["TOK_DIR"] = str(tmp_path)
    # Ensure uv env vars are set so the guard passes
    env["VIRTUAL_ENV"] = "1"

    proc = subprocess.Popen(
        [sys.executable, str(wrapper), "--time", "60"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    proc.stdin.write(b"testpass\n")
    proc.stdin.flush()

    # Wait for the copy OSC 52 sequence to appear
    expected_copy = base64.b64encode(b"my-secret-token").decode()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if osc_log.exists() and expected_copy in osc_log.read_text():
            break
        time.sleep(0.1)

    assert osc_log.exists() and expected_copy in osc_log.read_text(), \
        "secret was not copied via OSC 52"

    proc.send_signal(signal.SIGTERM)
    proc.wait(timeout=5)

    # After SIGTERM the clear sequence (payload "!") should appear
    content = osc_log.read_text()
    assert "\033]52;c;!\a" in content, "clipboard was not cleared after signal"
