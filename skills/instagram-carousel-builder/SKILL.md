---
name: instagram-carousel-builder
description: "Build 6-10 slide Instagram carousels in portrait 4:5 ratio (1080x1350). Formats Slide 1 (Primary Hook), Slide 2 (Second-Chance Algorithmic Re-serve Hook), Slides 3-N (Value Architecture), and Final Slide (Save & Share CTA). Generates slide text, layout hierarchy, and visual prompts. Use when creating carousels. Not for video Reels (use instagram-reel-scripter)."
---

# Instagram Carousel Builder

Carousels generate the highest save rates and dwell time on Instagram. This skill designs 6–10 slide visual storyboards optimized for swipe-through completion.

## The 4:5 Portrait Mandate
Always build in **4:5 aspect ratio (1080x1350 px)**. Square (1:1) wastes 25% of mobile screen real estate and decreases swipe conversion.

## Carousel Architecture

### Slide 1: The Primary Hook
- Giant high-contrast headline (under 10 words).
- Visual graphic, icon, or bold metric.
- Subtle swipe indicator (`Desliza →` or swipe dot).

### Slide 2: The Second-Chance Hook
- **Crucial 2026 Algorithmic Mechanic:** Instagram re-serves this carousel to followers who didn't swipe Slide 1, showing Slide 2 instead.
- Must stand alone as a compelling mini-hook or instant deliverable, not a generic intro.

### Slides 3 to 7 (The Meat):
- One clear concept per slide.
- Maximum 25–40 words per slide.
- High visual hierarchy: Bold Subheading + 2 bullet points or comparison box.

### Final Slide: Conversion & Action
- Summary checklist.
- Clear action prompt: "Guarda este carrusel para tener el paso a paso a mano" + "Compártelo con tu equipo".
- Profile tag (`@tuhandle`).

## Step-by-Step Flow

1. Choose a framework or comparison topic (e.g. from `../../references/creator-topics.md`).
2. Draft the slide deck (titles, body text, visual notes).
3. Draft the supporting caption and 3–5 niche hashtags.
4. Render the storyboard approval card using:
   `lib.render_approval_card(kind="carousel", slides=slides, preview_text=caption)`
5. (Optional) If Pixfaro key is set, generate slide mockups with `lib.illustrate_carousel([prompt1, prompt2, ...])`.
6. On approval, dispatch to Publora via `lib.publish(kind="carousel", ...)` or deliver for manual layout.
