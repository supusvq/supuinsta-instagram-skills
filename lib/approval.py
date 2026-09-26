"""Instagram Approval Gate Helpers.

Every skill producing Instagram content MUST present a structured draft to the
user and wait for explicit approval before publishing or scheduling.
"""
from __future__ import annotations
from typing import Any, Optional, Sequence


def render_approval_card(
    *,
    kind: str,  # "reel" | "carousel" | "post" | "story" | "comment" | "reply"
    preview_text: str,
    target_url: Optional[str] = None,
    media_specs: Optional[dict[str, Any]] = None,
    slides: Optional[Sequence[dict[str, str]]] = None,
    scenes: Optional[Sequence[dict[str, str]]] = None,
    hashtags: Optional[Sequence[str]] = None,
    char_count: Optional[int] = None,
    extra_context: Optional[dict[str, Any]] = None,
) -> str:
    """Format a standardized Instagram approval card."""
    lines = [f"## Draft Ready for Approval — Instagram {kind.upper()}", ""]

    if target_url:
        lines.append(f"**Target URL:** {target_url}")

    if char_count is None:
        char_count = len(preview_text)
    lines.append(f"**Caption Length:** {char_count} chars (Hook in first 125 chars)")

    if hashtags:
        lines.append(f"**Hashtags ({len(hashtags)}):** {' '.join(hashtags)}")

    lines.append("")

    # If it's a Reel script with scenes
    if scenes:
        lines.append("### 🎬 Reel Production Script (9:16)")
        lines.append("| Timing | Visual / Action | Spoken Audio | On-Screen Text Overlay |")
        lines.append("|---|---|---|---|")
        for sc in scenes:
            t = sc.get("time", "0:00")
            vis = sc.get("visual", "").replace("|", "/")
            aud = sc.get("audio", "").replace("|", "/")
            txt = sc.get("text", "").replace("|", "/")
            lines.append(f"| {t} | {vis} | {aud} | **{txt}** |")
        lines.append("")

    # If it's a Carousel with slides
    if slides:
        lines.append(f"### 📑 Carousel Storyboard ({len(slides)} Slides — 4:5 Aspect Ratio)")
        for idx, s in enumerate(slides, start=1):
            title = s.get("title", f"Slide {idx}")
            body = s.get("content", "")
            vis = s.get("visual_prompt", "")
            lines.append(f"**Slide {idx}: {title}**")
            if body:
                lines.append(f"> {body}")
            if vis:
                lines.append(f"*Visual Prompt:* `{vis}`")
            lines.append("")

    # Caption preview
    lines.append("### 📝 Caption Preview:")
    lines.append("")
    for pl in preview_text.splitlines() or [""]:
        lines.append(f"> {pl}")
    lines.append("")

    if media_specs:
        lines.append("### 🎨 Media Specifications:")
        for k, v in media_specs.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    if extra_context:
        lines.append("### ℹ️ Context:")
        for k, v in extra_context.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    lines.append("---")
    lines.append("Reply **post** / **yes** to publish, or suggest edits.")
    return "\n".join(lines)
