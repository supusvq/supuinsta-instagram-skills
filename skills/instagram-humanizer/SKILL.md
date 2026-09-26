---
name: instagram-humanizer
description: "Remove AI tells, robotic influencer clichés, and emoji vomit from Instagram captions and scripts. Audits line 1 against the 125-character mobile fold, ensures natural conversational cadence, checks hashtag density (3-5 max), and runs pre-publish audits. Use to scrub AI tone or review drafts before posting."
---

# Instagram Humanizer

Cleanses drafts of generic AI patterns, corporate stiffness, and outdated influencer tropes to ensure authentic creator resonance.

## What This Skill Scrubs

1. **Influencer & AI Clichés (Banned):**
   - "¡Hola comunidad!" / "¡Hola a todos!"
   - "En este post te voy a contar el secreto definitivo..."
   - "Descubre cómo revolucionar tu negocio..."
   - "Guarda este post antes de que lo borren..."
   - "No te lo puedes perder", "Un antes y un después".

2. **Emoji Vomit:**
   - Deletes stacked emoji chains (`🚀🔥✨💪💯`).
   - Caps emojis to 1–3 per caption, serving only as functional list bullets (`→`, `•`, `👇`).

3. **Sentence Pacing:**
   - Replaces artificial staccato ("Fácil. Rápido. Brutal.") with natural, thoughtful cadence.
   - Enforces double line breaks between paragraphs for mobile comfort.

## Modes

```bash
# Default rewrite mode:
instagram-humanizer <caption_or_script>

# Audit mode (pass/fail checklist, no rewrite):
instagram-humanizer --mode audit <text>

# Profile mode (builds voice-profile.md from 3-5 real posts):
instagram-humanizer --mode profile
```

## The 2026 Instagram Audit Checklist (`--mode audit`)

- [ ] **Line 1 Hook:** Under 125 characters? Does it create tension without clickbait?
- [ ] **Mobile Layout:** Are there double line breaks between ideas?
- [ ] **Emoji Count:** <= 3 total? Zero consecutive chains?
- [ ] **Hashtags:** Between 3 and 5 niche tags at the bottom?
- [ ] **CTA:** Clear, singular action (Save, Share, or Keyword DM)?
- [ ] **First-Person Authenticity:** Does it cite real proof or experience?
