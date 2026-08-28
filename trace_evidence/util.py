from __future__ import annotations
import hashlib, json, mimetypes, os, subprocess
from pathlib import Path
from datetime import datetime, timezone

MAGIC = {
    b'%PDF-': 'PDF document', b'PK\x03\x04': 'ZIP/container (possibly DOCX/XLSX/PPTX)',
    b'\x89PNG\r\n\x1a\n': 'PNG image', b'\xff\xd8\xff': 'JPEG image',
    b'GIF87a': 'GIF image', b'GIF89a': 'GIF image', b'\x7fELF': 'ELF executable',
    b'MZ': 'PE/Windows executable', b'\x1f\x8b': 'GZIP compressed data',
}

def sha256(path: Path, chunk=1024*1024):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(chunk), b''): h.update(b)
    return h.hexdigest()

def iso(ts: float): return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
def now_iso(): return datetime.now(timezone.utc).isoformat()

def detect_type(path: Path):
    try:
        head=path.read_bytes()[:16]
        for magic,label in MAGIC.items():
            if head.startswith(magic): return label
    except OSError: pass
    return mimetypes.guess_type(path.name)[0] or 'unknown'

def entropy(path: Path, sample=1024*1024):
    try:
        data=path.read_bytes()[:sample]
        if not data: return 0.0
        counts=[0]*256
        for b in data: counts[b]+=1
        import math
        n=len(data)
        return -sum((c/n)*math.log2(c/n) for c in counts if c)
    except OSError: return None

def safe_copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(src, dst)

def run_command(args, timeout=30):
    try:
        p=subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return p.stdout, p.stderr, p.returncode
    except (OSError, subprocess.TimeoutExpired) as e:
        return '', str(e), -1

def json_dump(path, obj): Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
