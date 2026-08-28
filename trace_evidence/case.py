from __future__ import annotations
import json, uuid, platform
from pathlib import Path
from trace_evidence.util import now_iso, sha256, json_dump

class Case:
    def __init__(self, root, case_id=None):
        self.root=Path(root); self.case_id=case_id or f"CASE-{uuid.uuid4().hex[:8].upper()}"
        self.root.mkdir(parents=True,exist_ok=True)
    def init(self):
        for d in ('evidence','artifacts','reports','logs'): (self.root/d).mkdir(exist_ok=True)
        manifest={'case_id':self.case_id,'created_at':now_iso(),'platform':platform.platform(),'tool':'TRACE','version':'1.0.0'}
        json_dump(self.root/'case.json',manifest); return manifest
    def register_evidence(self, path):
        p=Path(path); rows=[]
        for f in p.rglob('*') if p.is_dir() else [p]:
            if f.is_file():
                try: rows.append({'path':str(f.relative_to(p)) if p.is_dir() else f.name,'size':f.stat().st_size,'sha256':sha256(f)})
                except OSError: pass
        manifest={'case_id':self.case_id,'registered_at':now_iso(),'evidence_root':str(p.resolve()),'files':rows}
        json_dump(self.root/'evidence-manifest.json',manifest); return manifest
    def verify(self):
        m=json.loads((self.root/'evidence-manifest.json').read_text())
        root=Path(m['evidence_root']); results=[]
        for x in m['files']:
            f=root/x['path']; status='MISSING'
            if f.exists():
                try: status='OK' if sha256(f)==x['sha256'] else 'MODIFIED'
                except OSError: status='UNREADABLE'
            results.append({**x,'status':status})
        return results
