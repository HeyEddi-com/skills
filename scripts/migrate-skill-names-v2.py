#!/usr/bin/env python3
"""Hub wrapper — delegates to @heyeddi-orchestrator migrate_heyeddi tool."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MIGRATE = REPO_ROOT / "skills" / "heyeddi-orchestrator" / "scripts" / "migrate_heyeddi.py"


def main() -> None:
    args = sys.argv[1:]
    if not MIGRATE.is_file():
        print(f"error: {MIGRATE} not found", file=sys.stderr)
        sys.exit(1)
    result = subprocess.run([sys.executable, str(MIGRATE), *args], check=False)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
