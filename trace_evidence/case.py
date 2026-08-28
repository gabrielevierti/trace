from __future__ import annotations
import json, platform, socket, getpass
from datetime import datetime, timezone
from pathlib import Path
from trace_evidence.util import sha256_file

def manifest(case_dir, files):
    p=Path(case_dir); p.mkdir(parents=True,exist_ok=True)
    items=[]
    for f in files:
        fp=Path(f)
        if fp.exists() and fp.is_file(): items.append({'path':str(fp.resolve()),'size':fp.stat().st_size,'sha256':sha256_file(fp)})
    data={'trace_version':'0.3.0','case_id':p.name,'created_at':datetime.now(timezone.utc).isoformat(),'host':{'system':platform.system(),'release':platform.release(),'hostname':socket.gethostname(),'user':getpass.getuser()},'files':items}
    out=p/'manifest.json'; out.write_text(json.dumps(data,indent=2),encoding='utf-8'); return out

def verify(manifest_path):
    data=json.loads(Path(manifest_path).read_text(encoding='utf-8')); results=[]
    for item in data.get('files',[]):
        p=Path(item['path']); exists=p.exists(); actual=sha256_file(p) if exists and p.is_file() else None
        results.append({'path':str(p),'status':'OK' if actual==item['sha256'] else ('MISSING' if not exists else 'MODIFIED'),'expected':item['sha256'],'actual':actual})
    return results
