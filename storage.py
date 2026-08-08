import json
from pathlib import Path

STATE_FILE = Path("data/seen.json")

def load_seen() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

def save_seen(seen: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    # Keep the file reasonably small.
    if len(seen) > 5000:
        items = sorted(seen.items(), key=lambda x: x[1].get("first_seen", ""))
        seen = dict(items[-4000:])
    STATE_FILE.write_text(
        json.dumps(seen, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
