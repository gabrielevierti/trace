from __future__ import annotations
import sqlite3, shutil, tempfile
from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.util import stable_id
EPOCH=11644473600

def chrome_time(v):
    try:
        from datetime import datetime, timezone
        return datetime.fromtimestamp(v/1_000_000-EPOCH,timezone.utc).isoformat()
    except Exception:return None

def parse(path):
    path=Path(path).expanduser(); out=[]
    if not path.exists():return out
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        try: shutil.copy2(path,tmp.name); con=sqlite3.connect(tmp.name)
        except Exception:return out
        try:
            for row in con.execute('SELECT id,url,title,last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 5000'):
                i,url,title,ts=row; out.append(Artifact(stable_id('chrome_visit',i,url), 'browser_visit','chrome',title or url,chrome_time(ts),None,None,{'url':url,'title':title or ''}))
            for row in con.execute('SELECT id,target_path,current_path,tab_url,referrer,last_access_time FROM downloads ORDER BY last_access_time DESC LIMIT 5000'):
                i,target,current,url,ref,ts=row; p=current or target; out.append(Artifact(stable_id('chrome_download',i,p,ts),'download','chrome',Path(p).name,p and chrome_time(ts),p,None,{'url':url or '', 'referrer':ref or '', 'target_path':target or '', 'current_path':current or ''}))
        finally: con.close()
    return out
