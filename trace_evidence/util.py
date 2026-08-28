from __future__ import annotations
import hashlib
from pathlib import Path
from datetime import datetime, timezone

def sha256(path: Path, chunk=1024*1024):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b = f.read(chunk)
            if not b: break
            h.update(b)
    return h.hexdigest()

def iso(ts: float):
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
