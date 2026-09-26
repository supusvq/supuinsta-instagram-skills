"""Instagram URL parser.

Handles common shapes:
1. Post / Carousel URL:
   https://www.instagram.com/p/C_abc123XYZ/
2. Reel URL:
   https://www.instagram.com/reel/DA_xyz789ABC/
3. Story URL:
   https://www.instagram.com/stories/username/123456789012345/
4. Profile URL:
   https://www.instagram.com/username/
5. Comment query param:
   ?comment_id=180123456789

Returns normalized dict:
    {
      "shortcode": "C_abc123XYZ" | None,
      "url_type": "post" | "reel" | "story" | "profile" | "unknown",
      "username": "username" | None,
      "comment_id": "180123456789" | None,
      "canonical_url": str,
    }
"""
from __future__ import annotations
import re
from urllib.parse import urlparse, parse_qs, unquote
from typing import Optional, TypedDict


class ParsedInstagramUrl(TypedDict, total=False):
    shortcode: Optional[str]
    url_type: str
    username: Optional[str]
    comment_id: Optional[str]
    canonical_url: str


POST_RE = re.compile(r"/p/([A-Za-z0-9_-]+)")
REEL_RE = re.compile(r"/reel/([A-Za-z0-9_-]+)")
STORY_RE = re.compile(r"/stories/([A-Za-z0-9_.-]+)/(\d+)")
PROFILE_RE = re.compile(r"^/([A-Za-z0-9_.-]+)/?$")

RESERVED_PATHS = {
    "explore", "reels", "stories", "direct", "accounts", "legal", "about",
    "help", "developer", "api", "p", "reel", "tv"
}


def parse_instagram_url(url: str) -> ParsedInstagramUrl:
    """Parse any Instagram URL into structured metadata."""
    decoded = unquote(url.strip())
    parsed_uri = urlparse(decoded)
    path = parsed_uri.path
    query = parse_qs(parsed_uri.query)

    comment_id = None
    if "comment_id" in query and query["comment_id"]:
        comment_id = query["comment_id"][0]

    out: ParsedInstagramUrl = {
        "shortcode": None,
        "url_type": "unknown",
        "username": None,
        "comment_id": comment_id,
        "canonical_url": url,
    }

    # Reel check
    m_reel = REEL_RE.search(path)
    if m_reel:
        code = m_reel.group(1)
        out["shortcode"] = code
        out["url_type"] = "reel"
        out["canonical_url"] = f"https://www.instagram.com/reel/{code}/"
        return out

    # Post / Carousel check
    m_post = POST_RE.search(path)
    if m_post:
        code = m_post.group(1)
        out["shortcode"] = code
        out["url_type"] = "post"
        out["canonical_url"] = f"https://www.instagram.com/p/{code}/"
        return out

    # Story check
    m_story = STORY_RE.search(path)
    if m_story:
        user, sid = m_story.groups()
        out["username"] = user
        out["shortcode"] = sid
        out["url_type"] = "story"
        out["canonical_url"] = f"https://www.instagram.com/stories/{user}/{sid}/"
        return out

    # Profile check
    m_prof = PROFILE_RE.match(path)
    if m_prof:
        u = m_prof.group(1)
        if u.lower() not in RESERVED_PATHS:
            out["username"] = u
            out["url_type"] = "profile"
            out["canonical_url"] = f"https://www.instagram.com/{u}/"
            return out

    return out


if __name__ == "__main__":
    import json
    import sys

    test_urls = sys.argv[1:] or [
        "https://www.instagram.com/p/DAq4XYZ123/?img_index=1",
        "https://www.instagram.com/reel/C_789abc_DEF/?igsh=abc123xyz",
        "https://www.instagram.com/stories/juangallardo/3465123456789/",
        "https://www.instagram.com/supudigital/",
    ]
    for u in test_urls:
        print(f"URL: {u}")
        print(json.dumps(parse_instagram_url(u), indent=2))
        print("-" * 40)
