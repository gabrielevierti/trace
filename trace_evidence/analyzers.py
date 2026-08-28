from __future__ import annotations
from trace_evidence.model import Artifact
from trace_evidence.util import detect_type
from pathlib import Path
import zipfile

def analyze_files(artifacts):
    findings=[]
    for a in artifacts:
        if a.kind!='file': continue
        ext=Path(a.name).suffix.lower(); typ=(a.metadata or {}).get('type','')
        if ext and typ and ext in ('.exe','.dll') and 'PE/' not in typ:
            findings.append({'severity':'medium','title':'Extension/type mismatch','artifact_id':a.id,'detail':f'Extension {ext} does not match detected type {typ}.'})
        if isinstance(a.metadata.get('entropy'),float) and a.metadata['entropy']>=7.5 and a.metadata.get('size',0)>4096:
            findings.append({'severity':'low','title':'High-entropy file region','artifact_id':a.id,'detail':'Sample entropy is high; compression or encryption may be present. This is not proof of maliciousness.'})
        if ext=='.pdf' and a.metadata.get('size',0)>0:
            try:
                p=Path(a.path); data=p.read_bytes() if p.exists() and p.stat().st_size<50*1024*1024 else b''
                if b'/JavaScript' in data or b'/JS' in data:
                    findings.append({'severity':'medium','title':'PDF JavaScript indicator','artifact_id':a.id,'detail':'PDF bytes contain a JavaScript marker.'})
                if b'/EmbeddedFile' in data:
                    findings.append({'severity':'medium','title':'PDF embedded-file indicator','artifact_id':a.id,'detail':'PDF bytes contain an embedded-file marker.'})
            except OSError: pass
    return findings
