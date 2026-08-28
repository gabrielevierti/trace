from __future__ import annotations
import sqlite3, shutil, tempfile
from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.util import stable_id

def parse(path):
    path=Path(path).expanduser(); out=[]
    if not path.exists():return out
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        try: shutil.copy2(path,tmp.name); con=sqlite3.connect(tmp.name)
        except Exception:return out
        try:
            # Safari schema varies by macOS version; try common HistoryItems/HistoryVisits layouts.
            q='''SELECT hv.id, hi.url, hi.title, hv.visit_time FROM history_visits hv JOIN history_items hi ON hv.history_item=hi.id ORDER BY hv.visit_time DESC LIMIT 5000'''
            for i,url,title,ts in con.execute(q):
                # Safari timestamps are seconds since 2001-01-01.
                from datetime import datetime,timezone,timedelta
                try:t=(datetime(2001,1,1,tzinfo=timezone.utc)+timedelta(seconds=ts)).isoformat()
                except Exception:t=None
                out.append(Artifact(stable_id('safari_visit',i,url),'browser_visit','safari',title or url,t,None,None,{'url':url,'title':title or ''}))
        except Exception: pass
        finally: con.close()
    return out
