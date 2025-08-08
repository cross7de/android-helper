from pathlib import Path
import json
from ..constants import ctx

def ensure_dirs():
    ctx.state_dir.mkdir(parents=True, exist_ok=True)

def read_list_file(path: Path):
    items = []
    if path and Path(path).exists():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items.append(line)
    return items

def save_state(name: str, data):
    ensure_dirs()
    (ctx.state_dir / f"{name}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

def load_state(name: str, default):
    p = ctx.state_dir / f"{name}.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default
