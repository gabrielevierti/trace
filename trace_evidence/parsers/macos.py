from __future__ import annotations
import sqlite3, plistlib, json
from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.util import iso

def quarantine(path):
    p=Path(path).expanduser(); out=[]
    if not p.exists(): return out
    try:
        con=sqlite3.connect(p); con.row_factory=sqlite3.Row
        for r in con.execute('SELECT * FROM LSQuarantineEvent ORDER BY LSQuarantineTimeStamp DESC'):
            d=dict(r); url=d.get('LSQuarantineDataURLString'); name=d.get('LSQuarantineEventIdentifier') or (Path(url).name if url else 'quarantine-event')
            ts=d.get('LSQuarantineTimeStamp')
            out.append(Artifact(id=f"quarantine:{d.get('LSQuarantineEventIdentifier') or len(out)}",kind='quarantine_event',source='macos.quarantine',name=name,timestamp=str(ts) if ts else None,metadata=d))
        con.close()
    except sqlite3.Error: pass
    return out

def unified_log_text(path):
    p=Path(path); out=[]
    if not p.exists(): return out
    try:
        for i,line in enumerate(p.read_text(errors='replace').splitlines()):
            if not line.strip(): continue
            out.append(Artifact(id=f"unifiedlog:{i}",kind='log_event',source='macos.unified_log',name=line[:180],metadata={'message':line}))
    except OSError: pass
    return out
