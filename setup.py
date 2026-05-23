from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent

setup(
    name="telegram-dir-watcher",
    version="0.1.0",
    description="Watch a folder and send Telegram alerts.",
    long_description=(HERE / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="TopherBot",
    url="https://github.com/yourname/telegram-dir-watcher",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "watchdog>=3.0",
        "requests>=2.31",
    ],
    entry_points={"console_scripts": ["telegram-dir-watcher=telegram_dir_watcher.__main__:main"]},
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
