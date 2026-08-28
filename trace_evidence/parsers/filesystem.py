from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.util import sha256, iso, detect_type, entropy
import uuid

def scan(root: str, max_file_mb: int = 512):
    rootp=Path(root).expanduser().resolve(); artifacts=[]
    if not rootp.exists(): return artifacts
    for p in rootp.rglob('*'):
        if not p.is_file(): continue
        try:
            st=p.stat(); digest=sha256(p) if st.st_size<=max_file_mb*1024*1024 else None
            artifacts.append(Artifact(
                id=f"file:{uuid.uuid5(uuid.NAMESPACE_URL,str(p))}", kind='file', source='filesystem', name=p.name,
                path=str(p), sha256=digest, timestamp=iso(st.st_mtime),
                metadata={'size':st.st_size,'ctime':iso(st.st_ctime),'type':detect_type(p),'entropy':entropy(p) if st.st_size else 0.0}, observed=True))
        except (PermissionError,OSError): continue
    return artifacts
