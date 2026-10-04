"""Restore .github/copilot-instructions.md from git if it is missing.

The single source of truth is git history, not a copy embedded in this script
(an embedded copy drifts and previously restored a stale v2.1 policy).
"""

import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(REPO_ROOT, ".github", "copilot-instructions.md")
REL = ".github/copilot-instructions.md"


def main() -> int:
    if os.path.exists(TARGET):
        print(f"OK {TARGET} already exists. No action needed.")
        return 0
    try:
        result = subprocess.run(["git", "checkout", "--", REL], cwd=REPO_ROOT,
                                capture_output=True, text=True)
    except FileNotFoundError:
        result = None
    if result is not None and result.returncode == 0 and os.path.exists(TARGET):
        print(f"OK Restored {TARGET} from git.")
        return 0
    print(f"ERROR: could not restore {REL} from git. Run: git checkout -- {REL}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
