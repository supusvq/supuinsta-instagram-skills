#!/usr/bin/env python3
"""CLI: draft and post an Instagram comment on a target post/reel URL."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import parse_instagram_url, render_approval_card


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="Instagram post or reel URL")
    ap.add_argument("comment", help="Comment text to post")
    ap.add_argument("--dry-run", action="store_true", help="Preview only")
    args = ap.parse_args()

    parsed = parse_instagram_url(args.url)
    if parsed["url_type"] not in ("post", "reel"):
        print(f"✗ Could not identify a valid post or reel from: {args.url}", file=sys.stderr)
        return 2

    card = render_approval_card(
        kind="comment",
        preview_text=args.comment,
        target_url=parsed["canonical_url"],
    )
    print(card)
    print()

    if args.dry_run:
        print("(dry-run — nothing posted)")
        return 0

    ans = input("Publish comment? [yes/no]: ").strip().lower()
    if ans not in ("yes", "y", "post"):
        print("Cancelled.")
        return 0

    print("Instagram comments via API require user session or verified tool. Copy and paste:")
    print(f"\n{args.comment}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
