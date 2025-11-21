import re
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
routes = []

for routes_file in project_root.glob('app/**/routes.py'):
    text = routes_file.read_text(encoding='utf-8')
    lines = text.splitlines()
    last_blueprints = []
    for i, line in enumerate(lines):
        m = re.match(r"\s*@(\w+)\.route\(", line)
        if m:
            last_blueprints.append(m.group(1))
            continue
        mdef = re.match(r"\s*def\s+(\w+)\s*\(", line)
        if mdef and last_blueprints:
            func = mdef.group(1)
            for bp in last_blueprints:
                routes.append((routes_file.relative_to(project_root), bp, func))
            last_blueprints = []

# print summary
routes_sorted = sorted(routes, key=lambda r: (str(r[0]), r[1], r[2]))
print('Discovered routes (file, blueprint, function -> endpoint):')
for f, bp, fn in routes_sorted:
    print(f"{f} , {bp} , {fn} -> {bp}.{fn}")

# list unique blueprints
bps = sorted({r[1] for r in routes_sorted})
print('\nUnique blueprints found:')
for bp in bps:
    print('-', bp)
