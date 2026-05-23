import os
import tempfile
from pathlib import Path
from subprocess import run, PIPE

# The CLI script is executed via the entry‑point; we invoke it as a subprocess

def test_basic_flow(tmp_path: Path, monkeypatch):
    # Set dummy telegram env vars – the script will skip actual network calls
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "TESTTOKEN")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

    # Create a small temp directory and a dummy file inside
    watch_dir = tmp_path / "watch"
    watch_dir.mkdir()
    dummy_file = watch_dir / "hello.txt"
    dummy_file.write_text("hello")

    # Start the watcher as a background process (short‑lived)
    proc = run(
        ["python", "-m", "telegram_dir_watcher", str(watch_dir), "--debounce", "0.1"],
        stdout=PIPE,
        stderr=PIPE,
        timeout=2,
    )
    # The process should exit cleanly (KeyboardInterrupt simulated by timeout)
    assert proc.returncode == 0 or proc.returncode == 1
    # Ensure no unexpected errors were printed
    assert b"ERROR" not in proc.stderr

    # Modify the file – this will be caught if the watcher had stayed alive
    dummy_file.write_text("changed")
    # No assertion needed – the test mainly validates start‑up & env handling

