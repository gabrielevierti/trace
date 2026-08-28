from __future__ import annotations
import sqlite3, shutil, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
from trace_evidence.model import Artifact
EPOCH=datetime(2001,1,1,tzinfo=timezone.utc)
def safari_time(v):
    try: return (EPOCH+timedelta(seconds=float(v))).isoformat() if v is not None else None
    except (ValueError,TypeError,OverflowError): return None

def parse(history_path):
    src=Path(history_path).expanduser(); out=[]
    if not src.exists(): return out
    with tempfile.TemporaryDirectory() as d:
        copy=Path(d)/'History.db'; shutil.copy2(src,copy)
        con=sqlite3.connect(copy); con.row_factory=sqlite3.Row
        try:
            for r in con.execute('SELECT i.id,i.url,i.title,v.visit_time FROM history_items i JOIN history_visits v ON i.id=v.history_item'):
                out.append(Artifact(id=f"safari:visit:{r['id']}:{uuid.uuid4().hex[:8]}",kind='browser_visit',source='safari',name=(r['title'] or r['url'] or 'visit')[:160],timestamp=safari_time(r['visit_time']),metadata={'url':r['url']}))
        except sqlite3.Error: pass
        con.close()
    return out
