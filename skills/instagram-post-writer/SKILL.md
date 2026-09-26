---
name: instagram-post-writer
description: "Draft high-converting Instagram captions for Reels, Carousels, and Photos. Optimizes for the first 125 characters (mobile fold), skimmable double line-breaks, semantic SEO keywords, and high-save/high-share conversion. Use when the user wants to write an Instagram post or caption. Not for scripting video scenes (use instagram-reel-scripter) or slide-by-slide graphics (use instagram-carousel-builder)."
---

# Instagram Post & Caption Writer

Drafts Instagram captions that stop the scroll, drive saves and shares, and index naturally in Instagram search.

## When to Use
- User needs a caption for an upcoming Reel, Carousel, or Single Photo.
- User has an idea or topic and needs a strong 1-line hook + formatted body + CTA.
- User wants to optimize an existing caption for 2026 algorithm rules.

## Step-by-Step Flow

1. **Voice & Story Bank Check:**
   - Read `../../references/voice-profile.md`. If `filled: yes`, adopt the creator's rhythm and signature phrases.
   - Read `../../references/story-bank.md` to pull concrete metrics, client examples, or numbers.

2. **Select Asset Type & Hook:**
   - **Reel Caption:** 150–400 chars. Concise, summarizes key takeaway, reinforces the video.
   - **Carousel Caption:** 400–800 chars. Expands on the slides, provides extra nuance, ends with a Save CTA.
   - **Photo / Graphic Caption:** 500–1,000 chars. Micro-blog storytelling format.
   - Select a formula from `../../references/hook-formulas.md` (e.g. IH1, IH2, IH5).

3. **Draft the Caption:**
   - **Line 1 (Hook):** Under 125 characters. Stands alone, no greetings, presents the core tension or insight.
   - **Body:** Double line-breaks between every 1–2 sentences. Bullet points with `→` or `•`. Max 1–3 functional emojis (`👇`, `📌`, `👀`). No consecutive emoji chains.
   - **Call to Action (CTA):** Aligned with the goal:
     * Saves: "Guarda este post para tu próxima revisión técnica."
     * Shares: "Envíale esto a quien necesite optimizar su [tarea]."
     * DMs: "Comenta «PALABRA» y te envío el recurso completo por privado."
   - **Hashtags:** Exactly 3–5 hyper-specific niche tags at the bottom.

4. **Approval Card:**
   - Render using `lib.render_approval_card(kind="post", preview_text=draft, hashtags=tags)`.
   - Wait for explicit user confirmation.

5. **Publish / Schedule:**
   - On approval, dispatch via `lib.publish(kind="post", draft_text=draft, ...)`.
