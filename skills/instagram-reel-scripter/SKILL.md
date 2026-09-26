---
name: instagram-reel-scripter
description: "Script high-retention 15-45 second vertical Instagram Reels (9:16). Produces a 4-column production script: Timestamp, Visual/Action, Spoken Audio, and On-Screen Text Overlay. Optimizes for the critical 0-3 second retention threshold, sound-off viewers, and looping endings. Use when creating Reels. Not for text-only carousels (use instagram-carousel-builder)."
---

# Instagram Reel Scripter

Generates end-to-end production scripts for vertical video (9:16), engineered to maximize completion rate, re-watch loops, and direct DM shares.

## When to Use
- User wants to film a talking-head, screen recording, or b-roll Reel.
- User needs a strong 3-second hook (visual + audio + on-screen text).
- User wants to ensure the video works seamlessly with sound OFF.

## The 4-Column Script Structure

Every Reel script follows this standardized format:

| Timing | Visual / Action | Spoken Audio | On-Screen Text Overlay |
|---|---|---|---|
| **0:00–0:03 (Hook)** | [Dynamic movement, pattern interrupt, or pointing at screen] | "[First spoken hook sentence - under 12 words]" | **[BOLD 3-5 WORD HOOK]** |
| **0:03–0:12 (Tension)** | [Cut to screen demo or closer angle] | "[Explain the common error or the problem]" | [Key metric or obstacle] |
| **0:12–0:24 (The Fix)** | [Screencast / step-by-step resolution] | "[Deliver the core takeaway or mechanism]" | [Step 1 / Step 2 tags] |
| **0:24–0:30 (Loop/CTA)**| [Direct eye contact, smooth concluding gesture] | "[Final insight that loops back to the opening]" | **[SAVE / SHARE CTA]** |

## Rules for High Retention
1. **The 3-Second Filter:** 70% of swipe-aways happen before second 3. Never start by clearing your throat, saying "Hola chicos", or waving. Start mid-action.
2. **Sound-Off Viewers:** 68% watch on mute. The text overlay must communicate 100% of the core concept.
3. **Loop Construction:** If possible, write the final sentence so it grammatically connects into the first sentence, encouraging re-watches.
4. **Length Sweet Spot:** 20–35 seconds beats 60 seconds for 85%+ completion rates.

## Step-by-Step Flow
1. Identify the core message and target audience.
2. Select a hook formula from `../../references/hook-formulas.md` (e.g. IH1, IH4, IH6, IH14).
3. Draft the 4-column table.
4. Draft the complementary caption (150–300 chars) + 3-5 hashtags.
5. Render the approval card using `lib.render_approval_card(kind="reel", scenes=scenes, preview_text=caption)`.
6. Present to user for review and filming instructions.
