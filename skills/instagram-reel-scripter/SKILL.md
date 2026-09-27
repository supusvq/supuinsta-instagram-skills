---
name: instagram-reel-scripter
description: "Script high-retention 15-45 second vertical Instagram Reels (9:16). Produces a 4-column production script: Timestamp, Visual/Action, Spoken Audio, and On-Screen Text Overlay. Optimizes for the critical 0-3 second retention threshold, sound-off viewers, and looping endings. Use when creating Reels. Not for text-only carousels (use instagram-carousel-builder)."
---

# Instagram Reel Scripter

Generates end-to-end production scripts for vertical video (9:16), engineered to maximize completion rate, re-watch loops, and direct DM shares.

## Flujo Guiado para Principiantes ("A prueba de torpes")
Si el usuario simplemente dice "quiero hacer un reel" o "hazme un guión de vídeo", no le pidas tecnicismos. Pregúntale solo:
1. *"¿Qué truco, historia o lección quieres enseñar hoy? Cuéntamelo con tus palabras como si fuera una nota de voz."*
2. *"¿Cómo te gustaría grabarlo? (1: Tú hablando a cámara / 2: Grabando la pantalla del ordenador / 3: Vídeo de fondo con texto encima)"*
Con eso, el agente redacta el guión completo en 4 columnas listo para grabar en 30 segundos.

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
