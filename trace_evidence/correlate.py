from __future__ import annotations
from datetime import datetime
from pathlib import Path
from trace_evidence.model import Relationship


def parse_time(v):
    try:
        return datetime.fromisoformat(v) if v else None
    except (ValueError, TypeError):
        return None


def correlate(artifacts):
    files = [a for a in artifacts if a.kind == 'file']
    downloads = [a for a in artifacts if a.kind == 'download']
    visits = [a for a in artifacts if a.kind == 'browser_visit']
    rel = []
    seen = set()

    def add(r):
        key = (r.source_id, r.target_id, r.relation)
        if key not in seen:
            seen.add(key); rel.append(r)

    for d in downloads:
        for f in files:
            if not d.name or f.name.lower() != d.name.lower():
                continue
            basis = ['filename match']
            score = 0.62
            dt, ft = parse_time(d.timestamp), parse_time(f.timestamp)
            if dt and ft:
                delta = abs((ft - dt).total_seconds())
                if delta <= 5: score += .25; basis.append(f'timestamp proximity: {delta:.1f}s')
                elif delta <= 60: score += .14; basis.append(f'timestamp proximity: {delta:.1f}s')
            if d.path and f.path and Path(d.path).expanduser() == Path(f.path):
                score += .10; basis.append('exact target path match')
            add(Relationship(d.id, f.id, 'downloaded_as', min(score, .99), basis, True))

    # Correlate browser visits to downloads by URL host and time proximity when possible.
    for d in downloads:
        url = (d.metadata or {}).get('url') or ''
        if not url: continue
        for v in visits:
            vt, dt = parse_time(v.timestamp), parse_time(d.timestamp)
            if not vt or not dt: continue
            delta = abs((vt - dt).total_seconds())
            if delta <= 300:
                vurl = (v.metadata or {}).get('url') or ''
                from urllib.parse import urlparse
                if urlparse(url).netloc and urlparse(url).netloc == urlparse(vurl).netloc:
                    score = .78 if delta <= 30 else .66
                    basis = [f'timestamp proximity: {delta:.1f}s', 'same URL host']
                    add(Relationship(v.id, d.id, 'preceded_download', score, basis, True))
    return sorted(rel, key=lambda r: (-r.confidence, r.relation))
