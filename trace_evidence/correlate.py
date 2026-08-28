from __future__ import annotations
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from trace_evidence.model import Relationship

def parse_time(v):
    try: return datetime.fromisoformat(v) if v else None
    except (ValueError,TypeError): return None

def correlate(artifacts):
    files=[a for a in artifacts if a.kind=='file']; downloads=[a for a in artifacts if a.kind=='download']; visits=[a for a in artifacts if a.kind=='browser_visit']
    rel=[]; seen=set()
    def add(r):
        k=(r.source_id,r.target_id,r.relation)
        if k not in seen: seen.add(k); rel.append(r)
    for d in downloads:
        for f in files:
            if not d.name or f.name.lower()!=d.name.lower(): continue
            basis=['filename match']; score=.55
            dt,ft=parse_time(d.timestamp),parse_time(f.timestamp)
            if dt and ft:
                delta=abs((ft-dt).total_seconds())
                if delta<=5: score+=.30; basis.append(f'timestamp proximity: {delta:.1f}s')
                elif delta<=60: score+=.15; basis.append(f'timestamp proximity: {delta:.1f}s')
            if d.path and f.path and Path(d.path).expanduser()==Path(f.path): score+=.12; basis.append('exact target path match')
            add(Relationship(d.id,f.id,'downloaded_as',min(score,.99),basis,True))
    for d in downloads:
        du=(d.metadata or {}).get('url') or ''
        if not du: continue
        dh=urlparse(du).netloc
        for v in visits:
            vu=(v.metadata or {}).get('url') or ''; vh=urlparse(vu).netloc
            dt,vt=parse_time(d.timestamp),parse_time(v.timestamp)
            if not dh or dh!=vh or not dt or not vt: continue
            delta=abs((vt-dt).total_seconds())
            if delta<=300:
                score=.84 if delta<=30 else .68; basis=[f'timestamp proximity: {delta:.1f}s','same URL host']
                add(Relationship(v.id,d.id,'preceded_download',score,basis,True))
    return sorted(rel,key=lambda r:(-r.confidence,r.relation))
