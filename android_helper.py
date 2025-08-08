#!/usr/bin/env python3
from pathlib import Path
import sys

def _bootstrap_src() -> None:
    # Entwicklungsmodus: src/ ins sys.path einfügen, falls vorhanden
    here = Path(__file__).resolve().parent
    src = here / "src"
    if src.exists():
        sys.path.insert(0, str(src))

def run() -> int:
    _bootstrap_src()
    from android_helper.cli import main as cli_main  # Import nach Bootstrap
    return cli_main()

if __name__ == "__main__":
    raise SystemExit(run())
