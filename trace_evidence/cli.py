from __future__ import annotations
import argparse, json
from pathlib import Path
from trace_evidence.parsers.filesystem import scan
from trace_evidence.parsers.chrome import parse as parse_chrome
from trace_evidence.parsers.safari import parse as parse_safari
from trace_evidence.parsers.macos import quarantine, unified_log_text
from trace_evidence.parsers.usb import parse_system_profiler
from trace_evidence.correlate import correlate
from trace_evidence.analyzers import analyze_files
from trace_evidence.report import write_json, write_html, write_pdf
from trace_evidence.acquire import collect_macos
from trace_evidence.case import Case

CHROME=Path('~/Library/Application Support/Google/Chrome/Default/History').expanduser()
SAFARI=Path('~/Library/Safari/History.db').expanduser()
QUAR=Path('~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2').expanduser()

def analyze_cmd(args):
    root=Path(args.path).expanduser().resolve(); artifacts=scan(root,args.max_file_mb)
    if args.chrome: artifacts += parse_chrome(args.chrome_path or CHROME)
    if args.safari: artifacts += parse_safari(args.safari_path or SAFARI)
    if args.quarantine: artifacts += quarantine(args.quarantine_path or QUAR)
    for p in args.unified_log or []: artifacts += unified_log_text(p)
    for p in args.usb_profile or []: artifacts += parse_system_profiler(p)
    rel=correlate(artifacts); findings=analyze_files(artifacts)
    case={'case_id':args.case,'evidence_path':str(root),'analysis_version':'1.0.0'}
    write_json(args.json,artifacts,rel,findings,case); write_html(args.output,artifacts,rel,findings,case)
    if args.pdf: write_pdf(args.pdf,artifacts,rel,findings,case)
    print(f'TRACE analysis complete\nArtifacts: {len(artifacts)}\nRelationships: {len(rel)}\nFindings: {len(findings)}\nHTML: {args.output}\nJSON: {args.json}')

def main():
    p=argparse.ArgumentParser(prog='trace'); sub=p.add_subparsers(dest='cmd',required=True)
    c=sub.add_parser('collect-macos',help='Collect supported, user-readable macOS artifacts into a case directory')
    c.add_argument('--output',default='TRACE-CASE'); c.add_argument('--logs',action='store_true'); c.add_argument('--log-hours',type=int,default=1)
    a=sub.add_parser('analyze',help='Analyze an evidence directory')
    a.add_argument('path'); a.add_argument('--case',default='LOCAL-001'); a.add_argument('--chrome',action='store_true'); a.add_argument('--chrome-path'); a.add_argument('--safari',action='store_true'); a.add_argument('--safari-path'); a.add_argument('--quarantine',action='store_true'); a.add_argument('--quarantine-path'); a.add_argument('--unified-log',action='append'); a.add_argument('--usb-profile',action='append'); a.add_argument('--max-file-mb',type=int,default=512); a.add_argument('--json',default='trace-report.json'); a.add_argument('--output',default='trace-report.html'); a.add_argument('--pdf',default=None)
    v=sub.add_parser('verify',help='Verify a case evidence manifest'); v.add_argument('case')
    args=p.parse_args()
    if args.cmd=='collect-macos':
        cid,items=collect_macos(args.output,args.logs,args.log_hours); print(f'Created {cid} with {len(items)} collected sources.')
    elif args.cmd=='analyze': analyze_cmd(args)
    elif args.cmd=='verify':
        results=Case(args.case).verify(); print(json.dumps(results,indent=2)); print(f'OK: {sum(x["status"]=="OK" for x in results)}  MODIFIED: {sum(x["status"]=="MODIFIED" for x in results)}  MISSING: {sum(x["status"]=="MISSING" for x in results)}')
if __name__=='__main__': main()
