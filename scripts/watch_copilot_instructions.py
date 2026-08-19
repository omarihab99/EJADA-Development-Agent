"""Watch .github/copilot-instructions.md and restore it immediately if deleted."""

import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(REPO_ROOT, ".github", "copilot-instructions.md")

# Import the content from the restore script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from restore_copilot_instructions import CONTENT


def restore():
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "w", encoding="utf-8") as f:
        f.write(CONTENT)
    print(f"[watcher] Restored {TARGET}")


def watch():
    print(f"[watcher] Monitoring {TARGET} for deletion...")
    # Restore once at startup if missing
    if not os.path.exists(TARGET):
        restore()

    while True:
        time.sleep(1)
        if not os.path.exists(TARGET):
            restore()


if __name__ == "__main__":
    try:
        watch()
    except KeyboardInterrupt:
        pass
