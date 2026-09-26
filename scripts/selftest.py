#!/usr/bin/env python3
"""Selftest suite for instagram-skills."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib import (
    parse_instagram_url,
    render_approval_card,
    active_backend,
    image_backend,
    publish,
)


def test_url_parser():
    print("Testing URL parser...")
    p1 = parse_instagram_url("https://www.instagram.com/reel/DA_123xyz_9/")
    assert p1["url_type"] == "reel"
    assert p1["shortcode"] == "DA_123xyz_9"

    p2 = parse_instagram_url("https://www.instagram.com/p/C_abc456/?img_index=2")
    assert p2["url_type"] == "post"
    assert p2["shortcode"] == "C_abc456"

    p3 = parse_instagram_url("https://www.instagram.com/stories/juangallardo/3465123456789/")
    assert p3["url_type"] == "story"
    assert p3["username"] == "juangallardo"

    p4 = parse_instagram_url("https://www.instagram.com/supudigital/")
    assert p4["url_type"] == "profile"
    assert p4["username"] == "supudigital"
    print("✓ URL parser passed")


def test_approval_card():
    print("Testing approval card rendering...")
    card = render_approval_card(
        kind="carousel",
        preview_text="Line 1 Hook: Stop doing this manual task.\n\nHere is how to automate it.",
        slides=[
            {"title": "Hook", "content": "The 5-step automation", "visual_prompt": "Clean UI"},
            {"title": "Step 1", "content": "Connect the webhook", "visual_prompt": "Code block"},
        ],
        hashtags=["#automation", "#dev"],
    )
    assert "Draft Ready for Approval — Instagram CAROUSEL" in card
    assert "Carousel Storyboard (2 Slides" in card
    assert "#automation #dev" in card
    print("✓ Approval card passed")


def test_backend_dispatch():
    print("Testing backend dispatch in manual mode...")
    res = publish("post", "Test caption", "https://www.instagram.com/")
    assert res is not None
    assert res.get("mode") == "manual"
    assert "Test caption" in res["message"]
    print("✓ Backend dispatch passed")


def main():
    test_url_parser()
    test_approval_card()
    test_backend_dispatch()
    print("\nAll instagram-skills tests passed successfully! ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
