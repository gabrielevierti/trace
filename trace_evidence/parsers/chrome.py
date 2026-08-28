from __future__ import annotations
import sqlite3, shutil, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone
from trace_evidence.model import Artifact

CHROME_EPOCH = datetime(1601,1,1,tzinfo=timezone.utc)
def chrome_time(us):
    if not us: return None
    return (CHROME_EPOCH + __import__('datetime').timedelta(microseconds=us)).isoformat()

def parse(history_path: str):
    src=Path(history_path).expanduser()
    if not src.exists(): return []
    with tempfile.TemporaryDirectory() as d:
        copy=Path(d)/'History'; shutil.copy2(src, copy)
        con=sqlite3.connect(copy); con.row_factory=sqlite3.Row
        out=[]
        try:
            rows=con.execute('''SELECT d.guid,d.target_path,d.start_time,u.url,d.tab_url,d.total_bytes
                                FROM downloads d LEFT JOIN downloads_url_chains u ON d.id=u.id AND u.chain_index=0''').fetchall()
            for r in rows:
                path=r['target_path']; name=Path(path).name if path else 'unknown'
                out.append(Artifact(id=f"chrome:{r['guid'] or uuid.uuid4()}", kind='download', source='chrome', name=name,
                    path=path, timestamp=chrome_time(r['start_time']), metadata={'url':r['url'], 'tab_url':r['tab_url'], 'bytes':r['total_bytes']}))
        except sqlite3.Error: pass
        con.close(); return out
