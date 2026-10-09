#!/usr/bin/env python3
"""Delete archived log files dated before a cutoff.

Usage: purge_logs.py --before YYYY-MM-DD [--dry-run]
"""
import argparse
from datetime import date
from pathlib import Path

ARCHIVE = Path(__file__).resolve().parent.parent / "archive"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True, type=date.fromisoformat)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    old = sorted(p for p in ARCHIVE.glob("app-*.log")
                 if date.fromisoformat(p.stem[len("app-"):]) < args.before)
    for p in old:
        print(p.name)
        if not args.dry_run:
            p.unlink()
    verb = "would delete" if args.dry_run else "deleted"
    print(f"{verb} {len(old)} file(s)")


if __name__ == "__main__":
    main()
