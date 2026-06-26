#!/usr/bin/env python3
"""
Simple Skill Loader

Usage:
    python skill_loader.py list [SKILLS_DIR]
    python skill_loader.py show <skill_name> [SKILLS_DIR]
    python skill_loader.py match "<text>" [SKILLS_DIR]

This tool discovers SKILL.md files under SKILLS_DIR (default: ./skills),
parses a minimal YAML frontmatter (between the first two '---'), and exposes
search helpers so an agent can find and follow skill instructions.
"""
from pathlib import Path
import sys
import re
import json


def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def parse_frontmatter(text: str) -> dict:
    """Extract minimal frontmatter as lines between leading '---' markers.
    Returns a dict-like mapping for simple 'key: value' lines."
    fm = {}
    m = re.match(r"\s*---\s*(.*?)\s*---\s*", text, flags=re.S)
    if not m:
        return fm
    block = m.group(1)
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('>')
    return fm


def discover_skills(skills_dir: Path) -> dict:
    skills = {}
    if not skills_dir.exists():
        return skills
    for md in skills_dir.rglob('SKILL.md'):
        rel = md.relative_to(skills_dir)
        skill_key = str(rel.parent).replace('\\', '/').strip('/') or rel.stem
        text = read_file(md)
        fm = parse_frontmatter(text)
        skills[skill_key] = {
            'path': str(md.resolve()),
            'frontmatter': fm,
            'content': text,
        }
    return skills


def match_skill_by_text(skills: dict, text: str) -> dict:
    """Return skills sorted by simple keyword match score against the SKILL.md content."""
    scores = []
    q = text.lower()
    for name, info in skills.items():
        content = (info.get('content') or '').lower()
        score = 0
        # exact trigger hints
        if '/'+q in content or q in content:
            score += 20
        # count occurrences of words
        for token in re.findall(r"\w+", q):
            score += content.count(token)
        scores.append((score, name))
    scores.sort(reverse=True)
    return [(name, skills[name]) for score, name in scores if score > 0]


def print_list(skills: dict):
    for name, info in sorted(skills.items()):
        nm = info.get('frontmatter', {}).get('name', name)
        desc = info.get('frontmatter', {}).get('description', '')
        print(f"- {name} ({nm})")
        if desc:
            print(f"    {desc}")


def print_show(skills: dict, key: str):
    info = skills.get(key)
    if not info:
        # try fuzzy
        matches = [k for k in skills.keys() if key.lower() in k.lower() or key.lower() in (skills[k].get('frontmatter', {}).get('name','').lower())]
        if matches:
            for m in matches:
                print_show(skills, m)
            return
        print(f"Skill not found: {key}")
        return
    print(json.dumps({'skill': key, **info}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args[0]
    skills_dir = Path(args[-1]) if len(args) > 1 else Path('./skills')
    if cmd == 'list':
        skills = discover_skills(skills_dir)
        print_list(skills)
        sys.exit(0)
    elif cmd == 'show' and len(args) >= 2:
        key = args[1]
        skills = discover_skills(skills_dir)
        print_show(skills, key)
        sys.exit(0)
    elif cmd == 'match' and len(args) >= 2:
        query = args[1]
        skills = discover_skills(skills_dir)
        results = match_skill_by_text(skills, query)
        for name, info in results:
            print(f"{name}: {info.get('frontmatter', {}).get('name','')}")
        if not results:
            print("No matching skills found")
        sys.exit(0)
    else:
        print('Unknown command or missing args')
        print(__doc__)
        sys.exit(2)
