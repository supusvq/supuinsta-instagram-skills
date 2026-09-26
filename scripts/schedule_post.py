#!/usr/bin/env python3
"""CLI: schedule an approved Instagram post, carousel, or reel via Publora.

Usage:
    python scripts/schedule_post.py --file caption.txt --media URL [URL ...] [--time "2026-09-28T18:00:00Z"] [--dry-run]
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import active_backend, publish


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="Path to caption text file")
    ap.add_argument("--media", nargs="+", required=True, help="Hosted media URLs (1=photo/reel, 2-10=carousel)")
    ap.add_argument("--time", default=None, help="Scheduled time in ISO 8601 UTC format")
    ap.add_argument("--dry-run", action="store_true", help="Preview without scheduling")
    args = ap.parse_args()

    caption = Path(args.file).read_text(encoding="utf-8").strip()
    if not caption:
        print("✗ Caption file is empty", file=sys.stderr)
        return 2

    kind = "carousel" if len(args.media) > 1 else "post"
    print(f"Preparing {kind.upper()} ({len(args.media)} media files, {len(caption)} chars)...")

    if args.dry_run:
        print("(dry-run mode — nothing scheduled)")
        return 0

    res = publish(
        kind=kind,
        draft_text=caption,
        media_urls=args.media,
        scheduled_time=args.time,
    )
    print("Result:")
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
