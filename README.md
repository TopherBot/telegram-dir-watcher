# telegram-dir-watcher 📁➡️📨

A **single‑file** Python utility that monitors a directory (recursively) and pushes a Telegram notification whenever a file is created, modified or deleted.

---

## 🌟 Highlights
- Zero‑config: just export `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
- Works on Windows, macOS and Linux.
- Tiny dependency footprint – only `watchdog` and `requests`.
- Full GitHub Actions CI:
  - **Lint** with `flake8`
  - **Tests** with `pytest`
  - **Security** scan with `trivy` (container image)
  - **Coverage** badge
- MIT‑licensed, ready to fork.

---

## 🚀 Installation
```bash
# Using pip (recommended)
python -m pip install telegram-dir-watcher

# Or clone & installeditable for development
git clone https://github.com/yourname/telegram-dir-watcher.git
cd telegram-dir-watcher
python -m pip install -e .
```

Make sure you have a Telegram bot token and a chat ID:
```bash
export TELEGRAM_BOT_TOKEN='123456:ABC-DEF...'
export TELEGRAM_CHAT_ID='-1001234567890'
```

---

## 🛠️ Usage
```bash
# Watch the current directory
telegram-dir-watcher .
```
You can also specify a custom path and debounce interval:
```bash
telegram-dir-watcher /path/to/dir --debounce 2.5
```

---

## 📚 How it works
The script uses **watchdog** to receive file‑system events, de‑duplicates rapid bursts with a simple debounce timer, then posts a formatted message to Telegram via the Bot API.

---

## 🧪 Testing
```bash
# Run the test suite
pytest -q
```
Coverage threshold is enforced at 80% (see `pyproject.toml`).

---

## 🏗️ CI/CD (GitHub Actions)
The repository ships with a workflow at `.github/workflows/ci.yml` that runs on every push and PR:
- lint → `flake8`
- unit tests → `pytest --cov`
- security → `trivy` scans the built Docker image
- builds a lightweight Docker image (`python:3.12-slim`) for reproducible runs.

---

## 📜 License
MIT – see `LICENSE`.

---

## 🙋‍♂️ Contributing
Feel free to open issues or PRs! Please keep the CI green and add tests for new features.

---

## 📢 Badges (auto‑generated)
[![CI](https://github.com/yourname/telegram-dir-watcher/actions/workflows/ci.yml/badge.svg)](https://github.com/yourname/telegram-dir-watcher/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/yourname/xxxx/raw/coverage.json)](https://github.com/yourname/telegram-dir-watcher)
![License](https://img.shields.io/github/license/yourname/telegram-dir-watcher)
