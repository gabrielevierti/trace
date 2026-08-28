from __future__ import annotations
import plistlib
from pathlib import Path
from trace_evidence.model import Artifact

def parse_system_profiler(path):
    p=Path(path); out=[]
    if not p.exists(): return out
    try:
        data=plistlib.loads(p.read_bytes())
        items=data.get('_items',[]) if isinstance(data,dict) else []
        def walk(x):
            if isinstance(x,dict):
                if any(k in x for k in ('_name','serial_num','manufacturer')) and ('_name' in x or 'serial_num' in x):
                    name=str(x.get('_name') or x.get('name') or 'USB device')
                    out.append(Artifact(id=f"usb:{len(out)}",kind='usb_device',source='macos.system_profiler',name=name,metadata=x))
                for v in x.values(): walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(items)
    except Exception: return []
    return out
