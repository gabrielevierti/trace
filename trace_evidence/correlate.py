from __future__ import annotations
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from trace_evidence.model import Relationship

def parse_time(v):
    try:return datetime.fromisoformat(v.replace('Z','+00:00')) if v else None
    except Exception:return None

def correlate(artifacts):
    files=[a for a in artifacts if a.kind=='file']; downloads=[a for a in artifacts if a.kind=='download']; visits=[a for a in artifacts if a.kind=='browser_visit']
    rel=[]; seen=set()
    def add(r):
        k=(r.source_id,r.target_id,r.relation)
        if k not in seen:seen.add(k);rel.append(r)
    for d in downloads:
        for f in files:
            if not d.name or f.name.lower()!=d.name.lower():continue
            score=.55; basis=['filename match']; dt,ft=parse_time(d.timestamp),parse_time(f.timestamp)
            if dt and ft:
                delta=abs((ft-dt).total_seconds())
                if delta<=5:score+=.28;basis.append(f'timestamp proximity: {delta:.1f}s')
                elif delta<=60:score+=.15;basis.append(f'timestamp proximity: {delta:.1f}s')
            if d.path and f.path and Path(d.path).expanduser()==Path(f.path):score+=.12;basis.append('exact target path match')
            add(Relationship(d.id,f.id,'downloaded_as',min(score,.99),basis))
    for d in downloads:
        u=(d.metadata or {}).get('url',''); host=urlparse(u).netloc
        if not host:continue
        dt=parse_time(d.timestamp)
        for v in visits:
            vt=parse_time(v.timestamp); vh=urlparse((v.metadata or {}).get('url','')).netloc
            if dt and vt and host==vh:
                delta=abs((vt-dt).total_seconds())
                if delta<=300:
                    add(Relationship(v.id,d.id,'preceded_download',.80 if delta<=30 else .66,[f'timestamp proximity: {delta:.1f}s','same URL host']))
    return sorted(rel,key=lambda x:(-x.confidence,x.relation))
