import sys
import traceback
from pathlib import Path

try:
    # Ensure project root is on sys.path so `import app` works when script is run from tools/
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))

    # Import db object and monkeypatch create_all to no-op to avoid DB dependency
    from app import db
    db.create_all = lambda *a, **k: None

    from app import create_app
    app = create_app()

    print("Registered endpoints and rules:")
    rules = sorted(app.url_map.iter_rules(), key=lambda r: (r.endpoint, r.rule))
    for rule in rules:
        print(f"{rule.endpoint:40} {rule.rule}")
except Exception:
    print("Error while creating app or printing routes:")
    traceback.print_exc()
    sys.exit(1)
