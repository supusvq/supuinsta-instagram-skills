#!/usr/bin/env python3
"""Validate that all 12 skills have valid SKILL.md frontmatter."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"


def check_skill_md(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        print(f"✗ Missing frontmatter header: {path}")
        return False
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"✗ Malformed frontmatter: {path}")
        return False
    fm = parts[1]
    has_name = "name:" in fm
    has_desc = "description:" in fm
    if not (has_name and has_desc):
        print(f"✗ Incomplete frontmatter in {path} (needs name and description)")
        return False
    return True


def main() -> int:
    skills = [p for p in SKILLS_DIR.iterdir() if p.is_dir()]
    if len(skills) != 12:
        print(f"✗ Expected 12 skills, found {len(skills)}")
        return 1

    ok = True
    for s in sorted(skills):
        skill_file = s / "SKILL.md"
        if not skill_file.is_file():
            print(f"✗ Missing SKILL.md in {s.name}")
            ok = False
        else:
            if not check_skill_md(skill_file):
                ok = False

    root_skill = ROOT / "SKILL.md"
    if root_skill.is_file():
        if not check_skill_md(root_skill):
            ok = False

    if ok:
        print(f"✓ All {len(skills)} skills and root SKILL.md frontmatter are valid!")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
