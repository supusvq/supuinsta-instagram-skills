"""Instagram Publishing and Asset Generation Backend Selector.

Manages the 3 tiers:
- TIER 0: Manual (Default, zero setup). Returns formatted copy-paste caption and asset spec cards.
- TIER 1: Publora auto-post (requires PUBLORA_API_KEY + INSTAGRAM_PLATFORM_ID).
- TIER 2: DIY custom script (INSTAGRAM_SKILLS_CUSTOM_POSTER).
"""
from __future__ import annotations
import json
import os
import shlex
import subprocess
from typing import Any, Literal, Optional, Sequence

from ._env import load_env

load_env()

BackendName = Literal["publora", "manual", "diy"]
PublishKind = Literal["reel", "carousel", "post", "comment"]

PUBLORA_SIGNUP_URL = "https://app.publora.com/signup"
PIXFARO_SIGNUP_URL = "https://api.pixfaro.com/signup?ref=instagram-skills"

ASPECT_RATIOS = {
    "carousel": "4:5",
    "post": "4:5",
    "portrait": "4:5",
    "reel": "9:16",
    "story": "9:16",
    "square": "1:1",
}


def active_backend() -> BackendName:
    if os.getenv("PUBLORA_API_KEY") and (
        os.getenv("INSTAGRAM_PLATFORM_ID") or os.getenv("LINKEDIN_PLATFORM_ID")
    ):
        return "publora"
    if os.getenv("INSTAGRAM_SKILLS_CUSTOM_POSTER"):
        return "diy"
    return "manual"


def image_backend() -> Literal["pixfaro", "manual"]:
    if os.getenv("PIXFARO_TOKEN") or os.getenv("PIXFARO_API_KEY"):
        return "pixfaro"
    return "manual"


def manual_mode_message(
    draft_text: str,
    target_url: str = "https://www.instagram.com/",
    kind: str = "post",
    media_specs: Optional[dict[str, Any]] = None,
) -> str:
    """Format copy-paste instructions for the manual tier."""
    specs_block = ""
    if media_specs:
        specs_block = "\n**Media Specifications:**\n" + "\n".join(
            f"- **{k}**: {v}" for k, v in media_specs.items()
        ) + "\n"

    return f"""✅ Instagram draft approved!

Copy and paste the caption below into Instagram ({kind.upper()}):

```
{draft_text}
```
{specs_block}
**Target / Destination:** {target_url}

---

💡 **Automate publishing:**
You can auto-publish directly to Instagram via Publora:
1. Connect Instagram in Publora: {PUBLORA_SIGNUP_URL}
2. Add `PUBLORA_API_KEY` and `INSTAGRAM_PLATFORM_ID` to your `.env`
"""


def publish(
    kind: PublishKind,
    draft_text: str,
    target_url: str = "https://www.instagram.com/",
    **kwargs: Any,
) -> Optional[dict]:
    backend = active_backend()

    if backend == "manual":
        return {
            "mode": "manual",
            "message": manual_mode_message(
                draft_text, target_url, kind=kind, media_specs=kwargs.get("media_specs")
            ),
        }

    if backend == "publora":
        from .publora_client import PubloraClient

        client = PubloraClient()
        platform_id = kwargs.get("platform_id") or os.getenv("INSTAGRAM_PLATFORM_ID")
        if not platform_id:
            try:
                platform_id = client.resolve_instagram_platform_id()
            except Exception:
                platform_id = None

        if not platform_id:
            return {
                "mode": "manual",
                "message": manual_mode_message(
                    draft_text, target_url, kind=kind, media_specs=kwargs.get("media_specs")
                ),
            }

        platforms = kwargs.get("platforms") or [platform_id]
        return client.create_post(
            content=draft_text,
            platforms=platforms,
            media_urls=kwargs.get("media_urls"),
            scheduled_time=kwargs.get("scheduled_time"),
        )

    if backend == "diy":
        cmd = os.getenv("INSTAGRAM_SKILLS_CUSTOM_POSTER")
        if not cmd:
            return None
        payload = {
            "kind": kind,
            "draft_text": draft_text,
            "target_url": target_url,
            **kwargs,
        }
        argv = shlex.split(cmd) + [kind, target_url]
        proc = subprocess.run(
            argv,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=120,
        )
        return {
            "mode": "diy",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    raise ValueError(f"unknown backend: {backend!r}")


def unpublish(post_group_id: Optional[str]) -> Optional[dict]:
    """Cancel a scheduled post or draft before it is published."""
    if not post_group_id or active_backend() != "publora":
        return {"mode": "manual", "message": "Nothing scheduled to cancel."}
    from .publora_client import PubloraClient

    return PubloraClient().delete_post(post_group_id=post_group_id)


def fetch_post(url: str, **kwargs: Any) -> Optional[dict]:
    """Fetch post details via Apify."""
    if not os.getenv("APIFY_TOKEN"):
        return None
    try:
        from .apify_client import ApifyClient

        return ApifyClient().fetch_post(url, **kwargs)
    except Exception:
        return None


def fetch_comments(url: str, **kwargs: Any) -> Optional[list[dict[str, Any]]]:
    """Fetch comments via Apify."""
    if not os.getenv("APIFY_TOKEN"):
        return None
    try:
        from .apify_client import ApifyClient

        return ApifyClient().fetch_comments(url, **kwargs)
    except Exception:
        return None


def illustrate(
    prompt: str,
    kind: str = "carousel",
    *,
    aspect_ratio: Optional[str] = None,
    overlay: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Generate visual asset (defaults to 4:5 for Instagram)."""
    ar = aspect_ratio or ASPECT_RATIOS.get(kind, "4:5")
    if image_backend() == "manual":
        return {
            "backend": "manual",
            "message": (
                f"No Pixfaro key set. Generate the visual manually at {ar}:\n\n"
                f"Prompt:\n{prompt}\n\n"
                f"Tip: Set PIXFARO_TOKEN to generate automatically ({PIXFARO_SIGNUP_URL})."
            ),
        }
    from .pixfaro_client import PixfaroClient

    client = PixfaroClient()
    data = client.generate(prompt, aspect_ratio=ar, overlay=overlay, **kwargs)
    return {"backend": "pixfaro", "url": data.get("url"), "id": data.get("id")}


def illustrate_carousel(
    prompts: Sequence[str],
    *,
    overlay: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Generate all slide images for a multi-slide Instagram carousel (4:5)."""
    return [illustrate(p, kind="carousel", overlay=overlay, **kwargs) for p in prompts]


def quote_card(
    quote: str,
    *,
    name: Optional[str] = None,
    handle: Optional[str] = None,
    size: str = "4:5",
    **kwargs: Any,
) -> dict[str, Any]:
    """Render a crisp, HTML-typeset quote card."""
    if image_backend() == "manual":
        return {
            "backend": "manual",
            "message": f"Typeset manually ({size}):\n\n\"{quote}\" - {name or ''} {handle or ''}",
        }
    from .pixfaro_client import PixfaroClient

    client = PixfaroClient()
    slots = {"quote": quote}
    if name:
        slots["name"] = name
    if handle:
        slots["handle"] = handle
    data = client.render("quote-card", slots, size=size, **kwargs)
    return {"backend": "pixfaro", "url": data.get("url"), "id": data.get("id")}
