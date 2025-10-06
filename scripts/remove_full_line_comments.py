#!/usr/bin/env python3
"""
Recorre el workspace y elimina comentarios de línea completa en archivos de código:
- Python (.py): líneas que comienzan con optional whitespace + '#'
- Shell/Bash (.sh): same
- Dockerfile: lines starting with '#'
- SQL/.env/.md are left intact except full-line comments starting with '#'

NO toca docstrings (triple-quoted strings) ni elimina comentarios inline.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTS = ['.py', '.sh', 'Dockerfile', '.dockerfile']
modified = []

def is_dockerfile(path: Path):
    return path.name == 'Dockerfile' or path.suffix.lower() == '.dockerfile'

for p in ROOT.rglob('*'):
    try:
        if p.is_file():
            if is_dockerfile(p) or p.suffix in EXTS:
                text = p.read_text(encoding='utf-8')
                lines = text.splitlines()
                out_lines = []
                in_triple = False
                triple_chars = None
                for ln in lines:
                    stripped = ln.lstrip()
                    if p.suffix == '.py':
                        if not in_triple:
                            if stripped.startswith('"""') or stripped.startswith("'''"):
                                in_triple = True
                                triple_chars = stripped[:3]
                                out_lines.append(ln)
                                continue
                        else:
                            out_lines.append(ln)
                            if triple_chars and triple_chars in ln:
                                in_triple = False
                                triple_chars = None
                            continue
                    if stripped.startswith('#'):
                        # Keep shebangs and encoding lines
                        if stripped.startswith('#!') or 'coding' in stripped or 'utf-8' in stripped.lower():
                            out_lines.append(ln)
                        else:
                            continue
                    else:
                        out_lines.append(ln)
                new_text = '\n'.join(out_lines) + ('\n' if text.endswith('\n') else '')
                if new_text != text:
                    p.write_text(new_text, encoding='utf-8')
                    modified.append(str(p.relative_to(ROOT)))
    except Exception as e:
        print('Error processing', p, e)

print('Files modified:', len(modified))
for m in modified:
    print('-', m)
