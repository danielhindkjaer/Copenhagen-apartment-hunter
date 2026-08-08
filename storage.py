import json
from pathlib import Path
SEEN_FILE = Path("data/seen.json")

def load_seen():
    if not SEEN_FILE.exists(): return set()
    try: return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
    except Exception: return set()

def save_seen(seen):
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2), encoding="utf-8")
