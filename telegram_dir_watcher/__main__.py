import argparse
import os
import sys
import time
from pathlib import Path
from threading import Timer

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ---------------------------------------------------------------------------
# Helper: send a message to Telegram
# ---------------------------------------------------------------------------

def _send_telegram(message: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[WARN] Telegram credentials not set – skipping notification", file=sys.stderr)
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=5)
    except Exception as exc:  # pragma: no cover – network errors are rare in CI
        print(f"[ERROR] Telegram send failed: {exc}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Event handler with debounce
# ---------------------------------------------------------------------------

class DebouncedHandler(FileSystemEventHandler):
    def __init__(self, debounce: float):
        self.debounce = debounce
        self._timer: Timer | None = None
        self._events: list[str] = []

    def _flush(self):
        if self._events:
            payload = "\n".join(self._events)
            _send_telegram(f"<b>Directory change detected:</b>\n{payload}")
        self._events.clear()
        self._timer = None

    def _schedule(self, event_msg: str):
        self._events.append(event_msg)
        if self._timer:
            self._timer.cancel()
        self._timer = Timer(self.debounce, self._flush)
        self._timer.start()

    def on_created(self, event):
        if not event.is_directory:
            self._schedule(f"📂 Created: {Path(event.src_path).name}")

    def on_modified(self, event):
        if not event.is_directory:
            self._schedule(f"✏️ Modified: {Path(event.src_path).name}")

    def on_deleted(self, event):
        if not event.is_directory:
            self._schedule(f"🗑️ Deleted: {Path(event.src_path).name}")

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Watch a folder and send Telegram alerts.")
    parser.add_argument("path", nargs="?", default=".", help="Directory to watch (default: current directory)")
    parser.add_argument("--debounce", type=float, default=1.0, help="Debounce interval in seconds (default: 1.0)")
    args = parser.parse_args()

    watch_path = Path(args.path).resolve()
    if not watch_path.is_dir():
        print(f"[ERROR] {watch_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    event_handler = DebouncedHandler(debounce=args.debounce)
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=True)
    observer.start()
    print(f"👀 Watching {watch_path} (debounce={args.debounce}s)…")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 Stopping…")
    finally:
        observer.stop()
        observer.join()
        # Flush any pending events before exit
        if event_handler._timer:
            event_handler._timer.cancel()
        event_handler._flush()

if __name__ == "__main__":
    main()
