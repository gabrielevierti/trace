from __future__ import annotations
import os, shutil, json, stat
from pathlib import Path
from trace_evidence.case import Case
from trace_evidence.util import now_iso, safe_copy, run_command

MAC_SOURCES={
 'chrome':Path('~/Library/Application Support/Google/Chrome/Default/History').expanduser(),
 'safari':Path('~/Library/Safari/History.db').expanduser(),
 'quarantine':Path('~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2').expanduser(),
}

def collect_macos(output, include_logs=False, log_hours=1):
    root=Path(output); case=Case(root); case.init(); dest=root/'evidence'/'macos'; dest.mkdir(parents=True,exist_ok=True); manifest=[]
    for label,src in MAC_SOURCES.items():
        if src.exists():
            dst=dest/src.name; safe_copy(src,dst); dst.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH); manifest.append({'artifact':label,'source':str(src),'destination':str(dst),'acquired_at':now_iso()})
    out,err,code=run_command(['system_profiler','SPUSBDataType','-xml'],timeout=30)
    if code==0 and out:
        p=dest/'system_profiler_usb.xml'; p.write_text(out,encoding='utf-8'); manifest.append({'artifact':'usb_inventory','source':'system_profiler SPUSBDataType','destination':str(p),'acquired_at':now_iso()})
    if include_logs:
        out,err,code=run_command(['log','show','--last',f'{max(1,int(log_hours))}h','--style','syslog','--info','--debug'],timeout=90)
        if code==0 and out:
            p=dest/'unified.log.txt'; p.write_text(out,encoding='utf-8',errors='replace'); manifest.append({'artifact':'unified_log','source':f'log show --last {log_hours}h','destination':str(p),'acquired_at':now_iso()})
    (root/'chain-of-custody.log').write_text(f'[{now_iso()}] TRACE acquisition started\n' + ''.join(f'[{x["acquired_at"]}] collected {x["artifact"]} from {x["source"]} -> {x["destination"]}\n' for x in manifest), encoding='utf-8')
    (root/'acquisition.json').write_text(json.dumps({'case_id':case.case_id,'acquired_at':now_iso(),'sources':manifest},indent=2),encoding='utf-8')
    case.register_evidence(dest)
    return case.case_id,manifest
