# Project Conventions — instagram-skills (Claude Code)

This file governs Claude Code agents working with `instagram-skills`.

## Structure
- `SKILL.md`: Root bundle description.
- `skills/`: The 12 single-purpose skills.
- `.claude/skills/`: Relative symlinks to `../../skills/*` for automatic discovery.
- `references/`: Canonical algorithm heuristics, hook formulas, creator angles, and voice profile template.
- `lib/`: Python clients and glue logic (zero dependencies required for manual tier).
- `scripts/`: Self-tests and verification CLI tools.

## Development Workflow
1. When editing any skill, preserve the exact 12-skill invariant.
2. Ensure `references/voice-rules.md` is respected in all writing drafts.
3. Test changes locally with:
   `python3 scripts/selftest.py`
