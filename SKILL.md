---
name: instagram-marketing
description: "Plan, draft, storyboard, and publish Instagram Reels, Carousels, Stories, and Captions. Use when the user wants to script a viral Reel (visual+audio+overlay), build a 4:5 swipeable Carousel, write SEO-optimized captions (125-char mobile hook), audit a draft against 2026 Instagram algorithm heuristics (DM shares > saves > comments), plan a 30-day grid, or optimize an Instagram profile. Follows draft -> approval -> publish pattern."
---

# Instagram Marketing Skills

A bundle of 12 focused skills for Instagram content ops in 2026, built for Claude Code, Codex, and Antigravity. Each skill is single-purpose, follows the **draft → approval → publish** pattern, and supports the [Publora API](https://publora.com) for auto-posting.

## When to use this bundle

- **Writing a high-converting caption (Reel, Carousel, or Photo)** → use `instagram-post-writer`
- **Scripting a vertical Reel (0-3s hook, action, audio, text overlay)** → use `instagram-reel-scripter`
- **Building a slide-by-slide 4:5 Carousel storyboard** → use `instagram-carousel-builder`
- **Designing a 24h daily Story sequence (poll stickers, DM conversation triggers)** → use `instagram-story-strategist`
- **Reviewing a caption, removing AI buzzwords & emoji vomit, scoring readability** → use `instagram-humanizer`
- **Deconstructing why a viral Reel or Carousel performed** → use `instagram-hook-extractor`
- **Planning a 30-day or weekly Instagram content calendar** → use `instagram-content-planner`
- **Drafting value-first comments on niche creator accounts** → use `instagram-comment-drafter`
- **Managing post comment replies & converting engagers to DMs** → use `instagram-reply-handler`
- **Auditing and rewriting an Instagram bio, highlights & pinned posts** → use `instagram-profile-optimizer`
- **Repurposing a LinkedIn post, X thread, or blog post into Instagram formats** → use `instagram-repurposer`
- **Extracting real creator case studies & metrics into the Story Bank** → use `instagram-interviewer`

---

## The 2026 Instagram Distribution Reality

The Instagram algorithm underwent a structural shift in 2025–2026:
1. **DM Sends / Shares is the #1 viral signal.** When a user taps the paper airplane and shares a post to a friend or group chat, the algorithm weights that signal 5x–10x higher than a passive like. Content must provoke private conversation ("Have you seen this?", "We need this").
2. **Reels require 3-Second Hook Retention.** Over 70% of viewers must stay past second 0:03. This requires a synchronized Visual Hook + Spoken Audio Hook + Text-on-Screen.
3. **Carousels have the "Second-Chance" re-serve.** If Slide 1 is skipped, the feed re-serves the post with Slide 2 hours later. Slide 2 must act as an alternative hook.
4. **Captions: The 125-Character Fold.** On mobile, only the first 125 characters show before `... more`. Greetings and generic questions kill the click-through.
5. **SEO over Hashtag Stacking.** 3 to 5 targeted niche hashtags outperform 30 generic tags. The search engine parses caption text semantically.

---

## Core Operational Flow

### 🧙‍♂️ Modo Asistente Guiado ("A Prueba de Torpes" — Por Defecto)
Cuando el usuario haga una petición abierta o no técnica (por ejemplo: "quiero publicar algo", "hazme un post", "no sé qué subir"), **activa inmediatamente el Modo Asistente Guiado** (`references/guided-wizard.md`):
1. **No abrumes:** Haz máximo 1 o 2 preguntas a la vez con opciones numeradas (1, 2, 3) para que solo tenga que responder un número.
2. **Pide la idea en lenguaje coloquial:** Anima al usuario a contarlo con sus propias palabras, sin preocuparse por la redacción técnica.
3. **El agente hace todo el trabajo profesional:** Transforma esas respuestas sencillas en una pieza de ingeniería algorítmica de Instagram (Reel con guión en 4 columnas, Carrusel 4:5 slide a slide o copy optimizado con gancho de 125 caracteres).

Para peticiones técnicas avanzadas, sigue los tres pasos habituales:
1. **Parse & Contextualize:** URL parsing via `lib/url_parser.py` (Reel, Post, Carousel, or Story).
2. **Draft the Asset:** The skill applies 2026 heuristics (`references/algorithm-heuristics.md`, `references/hook-formulas.md`, `references/voice-rules.md`).
3. **Wait for Approval:** The user is presented with a structured approval card (`lib/approval.py`). No publishing or external call occurs without explicit user consent ("yes", "post", "publica").

---

## Three Tiers of Publishing

### 🟢 Tier 0 — Manual Draft (Default, Zero Setup)
Works out of the box with zero API keys. Every draft is returned as an approval card with exact media dimensions (4:5 or 9:16), scene timings, and copy-paste caption.

### 🔵 Tier 1 — Publora Auto-Post (Recommended)
On approval, posts and carousels are scheduled/published to Instagram via Publora:
1. Connect Instagram in [Publora](https://app.publora.com/signup).
2. Set credentials in `.env`:
   ```bash
   PUBLORA_API_KEY=sk_...
   INSTAGRAM_PLATFORM_ID=instagram-...
   ```

### ⚫ Tier 2 — DIY Custom Poster (Advanced)
Delegate publishing to a custom local command via `INSTAGRAM_SKILLS_CUSTOM_POSTER=<command>`.

---

## Optional Integrations

- **Apify (`APIFY_TOKEN`):** Scrapes Instagram post bodies, reel play counts, and comment threads without requiring login cookies.
- **Pixfaro (`PIXFARO_TOKEN`):** Generates 4:5 carousel slides, 9:16 vertical covers, and crisp typeset quote-cards automatically.

---

## Voice & Style Rules (Built-in)

- Line 1 hook under 125 chars.
- Max 1 to 3 functional emojis per post (no chains like `🚀🔥✨`).
- Double line-breaks between thoughts.
- Zero corporate or AI clichés ("en este post te cuento", "game changer", "contenido de valor").
- Always deliver the takeaway before asking for a save or follow.
