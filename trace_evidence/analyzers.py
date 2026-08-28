from __future__ import annotations
from trace_evidence.model import Artifact

def findings(artifacts):
    out=[]
    executable={'PE executable','ELF executable'}
    for a in artifacts:
        md=a.metadata or {}; detected=md.get('detected_type',''); ext=(md.get('extension') or '').lower()
        if a.kind=='file' and detected in executable and ext not in {'.exe','.dll','.sys','.bin','.elf',''}:
            out.append({'severity':'HIGH','title':'File signature / extension mismatch','artifact_id':a.id,'detail':f'{a.name} is detected as {detected} but has extension {ext or "(none)"}.','basis':['content signature','filesystem filename']})
        if a.kind=='file' and isinstance(md.get('entropy'),(int,float)) and md['entropy']>=7.6 and md.get('size',0)>=4096:
            out.append({'severity':'INFO','title':'High entropy region','artifact_id':a.id,'detail':f'{a.name} has sampled Shannon entropy {md["entropy"]}. High entropy can occur in compressed or encrypted data; it is not proof of maliciousness.','basis':['sampled byte entropy']})
        if a.kind=='file' and detected in executable:
            out.append({'severity':'INFO','title':'Executable content','artifact_id':a.id,'detail':f'{a.name} contains an executable file signature ({detected}).','basis':['content signature']})
    return out
