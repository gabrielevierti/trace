from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from trace_evidence.parsers.filesystem import scan
from trace_evidence.parsers.chrome import parse as parse_chrome
from trace_evidence.parsers.safari import parse as parse_safari
from trace_evidence.correlate import correlate
from trace_evidence.report import write_json,write_html
from trace_evidence.analyzers import findings
from trace_evidence.case import manifest,verify

def chrome_default():return Path('~/Library/Application Support/Google/Chrome/Default/History').expanduser()
def safari_default():return Path('~/Library/Safari/History.db').expanduser()

def analyze(args):
    artifacts=scan(args.path,args.max_files)
    if args.chrome:artifacts+=parse_chrome(args.chrome if isinstance(args.chrome,str) else chrome_default())
    if args.safari:artifacts+=parse_safari(args.safari if isinstance(args.safari,str) else safari_default())
    rel=correlate(artifacts); fs=findings(artifacts); write_json(args.json,artifacts,rel,fs); write_html(args.output,artifacts,rel,args.case,fs)
    print(f'Artifacts analyzed : {len(artifacts)}');print(f'Relationships       : {len(rel)}');print(f'HTML report         : {args.output}');print(f'JSON export         : {args.json}'); print(f'Findings            : {len(fs)}')
    for r in rel[:12]:print(f'  {r.relation:20} {r.confidence:5.0%}  {"; ".join(r.basis)}')

def main():
    p=argparse.ArgumentParser(prog='trace',description='TRACE — explainable digital evidence correlation engine')
    sp=p.add_subparsers(dest='cmd',required=True)
    a=sp.add_parser('analyze',help='Analyze a directory or file and generate an interactive report');a.add_argument('path');a.add_argument('--chrome',nargs='?',const=True,default=False,help='Parse Chrome History, or provide a database path');a.add_argument('--safari',nargs='?',const=True,default=False,help='Parse Safari History.db, or provide a database path');a.add_argument('--case',default='LOCAL ANALYSIS');a.add_argument('--max-files',type=int,default=10000);a.add_argument('--json',default='trace-report.json');a.add_argument('--output',default='trace-report.html');a.set_defaults(func=analyze)
    c=sp.add_parser('manifest',help='Create an integrity manifest for evidence files');c.add_argument('case_dir');c.add_argument('files',nargs='+');c.set_defaults(func=lambda x:print(manifest(x.case_dir,x.files)))
    v=sp.add_parser('verify',help='Verify files against a TRACE manifest');v.add_argument('manifest');v.set_defaults(func=lambda x: (print(json.dumps(verify(x.manifest),indent=2)),sys.exit(1 if any(r['status']!='OK' for r in verify(x.manifest)) else 0)))
    args=p.parse_args();args.func(args)
if __name__=='__main__':main()
