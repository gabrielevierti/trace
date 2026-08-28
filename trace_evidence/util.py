from __future__ import annotations
import hashlib, math, mimetypes, os, plistlib, re
from pathlib import Path
from datetime import datetime, timezone

MAGIC = [(b'%PDF-', 'PDF document'), (b'PK\x03\x04', 'ZIP/OOXML archive'), (b'\xFF\xD8\xFF', 'JPEG image'), (b'\x89PNG\r\n\x1a\n', 'PNG image'), (b'GIF8', 'GIF image'), (b'\x7fELF', 'ELF executable'), (b'MZ', 'PE executable')]

def sha256_file(path: Path, chunk=1024*1024):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(chunk): h.update(b)
    return h.hexdigest()

def detect_type(path: Path):
    try:
        with path.open('rb') as f: head=f.read(32)
    except OSError: return 'unreadable'
    for magic,name in MAGIC:
        if head.startswith(magic): return name
    return mimetypes.guess_type(path.name)[0] or 'unknown'

def entropy(path: Path, limit=1024*1024):
    try:
        data=path.read_bytes()[:limit]
    except OSError: return None
    if not data:return 0.0
    counts=[0]*256
    for b in data: counts[b]+=1
    n=len(data); return round(-sum((c/n)*math.log2(c/n) for c in counts if c),3)

def extract_strings(path: Path, minimum=6, limit=2*1024*1024):
    try:data=path.read_bytes()[:limit]
    except OSError:return []
    vals=re.findall(rb'[\x20-\x7e]{%d,}'%minimum,data)
    return [v.decode('utf-8','replace') for v in vals[:500]]

def iso(ts):
    if ts is None:return None
    return datetime.fromtimestamp(ts, timezone.utc).isoformat()

def stable_id(*parts):
    return hashlib.sha1('|'.join(str(x) for x in parts).encode()).hexdigest()[:16]

def plist_summary(path: Path):
    try:
        with path.open('rb') as f: obj=plistlib.load(f)
        if isinstance(obj,dict): return {str(k): str(v)[:300] for k,v in list(obj.items())[:40]}
    except Exception: pass
    return {}
