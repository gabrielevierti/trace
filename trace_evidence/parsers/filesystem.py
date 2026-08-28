from __future__ import annotations
from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.util import sha256_file, detect_type, entropy, iso, stable_id

def scan(root, max_files=10000):
    root=Path(root).expanduser().resolve(); out=[]
    if root.is_file(): paths=[root]
    else:
        paths=[]
        for p in root.rglob('*'):
            if p.is_file():
                paths.append(p)
                if len(paths)>=max_files: break
    for p in paths:
        try:
            st=p.stat(); digest=sha256_file(p)
            kind='file'
            md={'detected_type':detect_type(p),'size':st.st_size,'entropy':entropy(p),'extension':p.suffix.lower()}
            if p.suffix.lower() in {'.plist','.xml'}: md['plist_keys']=list(__import__('trace_evidence.util',fromlist=['plist_summary']).plist_summary(p).keys())[:20]
            if p.suffix.lower() in {'.pdf','.docx','.xlsx','.pptx','.zip'}: md['container']='archive/container candidate'
            out.append(Artifact(stable_id('file',p,digest),kind,'filesystem',p.name,iso(st.st_mtime),str(p),digest,md))
        except (OSError,PermissionError): continue
    return out
