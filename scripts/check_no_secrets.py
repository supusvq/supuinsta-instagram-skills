#!/usr/bin/env python3
"""Ensure no API keys, tokens, or private secrets are committed."""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUSPICIOUS_PATTERNS = [
    re.compile(r"sk_[a-zA-Z0-9_-]{20,}"),
    re.compile(r"pf_live_[a-zA-Z0-9_-]{20,}"),
    re.compile(r"apify_api_[a-zA-Z0-9_-]{20,}"),
]


def main() -> int:
    found = False
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name.startswith(".env") or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pat in SUSPICIOUS_PATTERNS:
                if pat.search(text):
                    print(f"✗ Potential secret in {path.relative_to(ROOT)}")
                    found = True
        except Exception:
            pass

    if found:
        return 1
    print("✓ No secrets detected across files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
