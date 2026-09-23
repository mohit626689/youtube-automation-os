#!/usr/bin/env python3
"""Root entrypoint for Universal YouTube Automation OS Setup."""
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
wizard_script = BASE_DIR / "scripts" / "setup_channel.py"

if __name__ == "__main__":
    subprocess.run([sys.executable, str(wizard_script)])
