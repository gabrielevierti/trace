from __future__ import annotations
import sqlite3, shutil, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone
from trace_evidence.model import Artifact

# Safari stores timestamps as seconds since 2001-01-01 in History.db
EPOCH = datetime(2001,1,1,tzinfo=timezone.utc)
def safari_time(v):
    if v is None: return None
    try: return (EPOCH + __import__('datetime').timedelta(seconds=float(v))).isoformat()
    except (ValueError, TypeError): return None

def parse(history_path: str):
    src=Path(history_path).expanduser()
    if not src.exists(): return []
    with tempfile.TemporaryDirectory() as d:
        copy=Path(d)/'History.db'; shutil.copy2(src, copy)
        con=sqlite3.connect(copy); con.row_factory=sqlite3.Row
        out=[]
        try:
            rows=con.execute('''SELECT i.id,i.url,i.title,v.visit_time FROM history_items i JOIN history_visits v ON i.id=v.history_item''').fetchall()
            for r in rows:
                name=(r['title'] or r['url'] or 'visit')[:160]
                out.append(Artifact(id=f"safari:{r['id']}:{uuid.uuid4()}", kind='browser_visit', source='safari', name=name,
                    timestamp=safari_time(r['visit_time']), metadata={'url':r['url']}))
        except sqlite3.Error: pass
        con.close(); return out
