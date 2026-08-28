from __future__ import annotations
import sqlite3, shutil, tempfile, uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta
from trace_evidence.model import Artifact
CHROME_EPOCH=datetime(1601,1,1,tzinfo=timezone.utc)
def chrome_time(us):
    if not us: return None
    try: return (CHROME_EPOCH+timedelta(microseconds=int(us))).isoformat()
    except (ValueError,TypeError,OverflowError): return None

def parse(history_path):
    src=Path(history_path).expanduser(); out=[]
    if not src.exists(): return out
    with tempfile.TemporaryDirectory() as d:
        copy=Path(d)/'History'; shutil.copy2(src,copy)
        con=sqlite3.connect(copy); con.row_factory=sqlite3.Row
        try:
            for r in con.execute('''SELECT d.id,d.guid,d.target_path,d.start_time,d.end_time,u.url,d.tab_url,d.total_bytes
              FROM downloads d LEFT JOIN downloads_url_chains u ON d.id=u.id AND u.chain_index=0'''):
                path=r['target_path']; name=Path(path).name if path else 'unknown'
                out.append(Artifact(id=f"chrome:download:{r['id']}",kind='download',source='chrome',name=name,path=path,timestamp=chrome_time(r['start_time']),metadata={'url':r['url'],'tab_url':r['tab_url'],'bytes':r['total_bytes'],'end_time':chrome_time(r['end_time'])}))
            for r in con.execute('SELECT id,url,title,last_visit_time FROM urls'):
                out.append(Artifact(id=f"chrome:visit:{r['id']}",kind='browser_visit',source='chrome',name=(r['title'] or r['url'] or 'visit')[:160],timestamp=chrome_time(r['last_visit_time']),metadata={'url':r['url']}))
        except sqlite3.Error: pass
        con.close()
    return out
