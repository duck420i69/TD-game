#!/usr/bin/env python3
"""
Agent-side Skill Router

Provides programmatic access to SKILL.md files under ./skills and a simple
trigger routing function for agent integrations (e.g., Copilot CLI agent).

API:
- load_skills(skills_dir: Path) -> dict
- match_skill(message: str, skills: dict) -> list of (score, name, info)
- route_trigger(message: str, skills_dir: Path) -> (name, info) | (None, None)

CLI:
  python agent_skill_router.py list
  python agent_skill_router.py route "compress file"

The router is intentionally simple (text-based matching). It is safe for an
LLM-based agent to call before executing any action: route_trigger returns the
best match and the full SKILL.md content to follow.
"""
from pathlib import Path
import re
import json
import sys


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _parse_frontmatter(text: str) -> dict:
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


def load_skills(skills_dir: Path = None) -> dict:
    skills_dir = Path(skills_dir or Path.cwd() / 'skills')
    skills = {}
    if not skills_dir.exists():
        return skills
    for md in skills_dir.rglob('SKILL.md'):
        rel = md.relative_to(skills_dir)
        name = str(rel.parent).replace('\\', '/').strip('/') or rel.stem
        text = _read(md)
        fm = _parse_frontmatter(text)
        skills[name] = {
            'path': str(md.resolve()),
            'frontmatter': fm,
            'content': text,
        }
    return skills


def match_skill(message: str, skills: dict) -> list:
    q = message.lower()
    scores = []
    tokens = re.findall(r"\w+", q)
    for name, info in skills.items():
        content = (info.get('content') or '').lower()
        score = 0
        # boost on exact trigger or name mentions
        if name.lower() in q:
            score += 10
        if '/' + name.lower() in content:
            score += 8
        # simple token frequency
        for t in tokens:
            score += content.count(t)
        scores.append((score, name, info))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


def route_trigger(message: str, skills_dir: Path = None, min_score: int = 1):
    skills = load_skills(skills_dir)
    if not skills:
        return None, None
    scores = match_skill(message, skills)
    if not scores:
        return None, None
    best_score, best_name, best_info = scores[0]
    if best_score < min_score:
        return None, None
    return best_name, best_info


def _cli_list(skills_dir: Path = None):
    skills = load_skills(skills_dir)
    for name, info in sorted(skills.items()):
        nm = info.get('frontmatter', {}).get('name', name)
        desc = info.get('frontmatter', {}).get('description', '')
        print(f"- {name} ({nm})")
        if desc:
            print(f"    {desc}")


def _cli_route(args):
    if not args:
        print('Usage: route "text" [skills_dir]')
        return
    text = args[0]
    skills_dir = Path(args[1]) if len(args) > 1 else None
    name, info = route_trigger(text, skills_dir)
    if not name:
        print('No matching skill found')
        return
    out = {'skill': name, 'frontmatter': info.get('frontmatter', {}), 'path': info.get('path')}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == 'list':
        skills_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        _cli_list(skills_dir)
    elif cmd == 'route':
        _cli_route(sys.argv[2:])
    else:
        print('Unknown command')
        print(__doc__)
        sys.exit(2)
