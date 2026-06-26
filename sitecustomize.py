"""
Auto-skill loader for Python-based agents.

This file runs automatically for Python interpreters that include the project
root in sys.path. On import it scans ./skills for SKILL.md files and writes a
cached JSON at .skills_cache/skills.json so external agents (or local tooling)
can read skills without invoking CLI scripts.

This is intentionally lightweight and safe: it only reads markdown files and
writes a JSON cache. It does not call external services or run untrusted code.
"""
from pathlib import Path
import json
import os

try:
    # Import the internal router if available
    from skills.caveman_compress.scripts.agent_skill_router import load_skills
except Exception:
    # fall back to direct discovery
    def load_skills(skills_dir=None):
        skills_dir = Path(skills_dir or Path.cwd() / 'skills')
        skills = {}
        if not skills_dir.exists():
            return skills
        for md in skills_dir.rglob('SKILL.md'):
            rel = md.relative_to(skills_dir)
            name = str(rel.parent).replace('\\', '/').strip('/') or rel.stem
            try:
                text = md.read_text(encoding='utf-8')
            except Exception:
                text = ''
            # minimal frontmatter parse
            fm = {}
            if text.startswith('---'):
                parts = text.split('---', 2)
                if len(parts) >= 3:
                    block = parts[1]
                    for line in block.splitlines():
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        if ':' in line:
                            k, v = line.split(':', 1)
                            fm[k.strip()] = v.strip().strip('>')
            skills[name] = {'path': str(md.resolve()), 'frontmatter': fm, 'content': text}
        return skills

# Build cache dir
cache_dir = Path('.skills_cache')
try:
    cache_dir.mkdir(exist_ok=True)
except Exception:
    cache_dir = Path.cwd()

skills = load_skills(Path('skills'))
cache_path = cache_dir / 'skills.json'
try:
    cache_path.write_text(json.dumps(skills, ensure_ascii=False, indent=2), encoding='utf-8')
    # Export env var for processes started from this Python interpreter
    os.environ['SKILLS_CACHE'] = str(cache_path.resolve())
except Exception:
    pass
