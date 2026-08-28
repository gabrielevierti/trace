from __future__ import annotations
import argparse
from pathlib import Path
from trace_evidence.parsers.filesystem import scan
from trace_evidence.parsers.chrome import parse as parse_chrome
from trace_evidence.parsers.safari import parse as parse_safari
from trace_evidence.correlate import correlate
from trace_evidence.report import write_json, write_html


def default_chrome(): return Path('~/Library/Application Support/Google/Chrome/Default/History').expanduser()
def default_safari(): return Path('~/Library/Safari/History.db').expanduser()


def main():
    p=argparse.ArgumentParser(prog='trace', description='Explainable digital evidence correlation engine')
    sub=p.add_subparsers(dest='cmd', required=True)
    a=sub.add_parser('analyze'); a.add_argument('path'); a.add_argument('--chrome', action='store_true'); a.add_argument('--safari', action='store_true'); a.add_argument('--json', default='trace-report.json'); a.add_argument('--output', default='trace-report.html')
    args=p.parse_args()
    print('TRACE — Digital Evidence Correlation Engine')
    artifacts=scan(args.path)
    if args.chrome:
        print(f'Reading Chrome: {default_chrome()}'); artifacts += parse_chrome(default_chrome())
    if args.safari:
        print(f'Reading Safari: {default_safari()}'); artifacts += parse_safari(default_safari())
    relationships=correlate(artifacts)
    write_json(args.json, artifacts, relationships); write_html(args.output, artifacts, relationships)
    print(f'Artifacts: {len(artifacts)}'); print(f'Relationships: {len(relationships)}'); print(f'JSON: {args.json}'); print(f'HTML: {args.output}')
    for r in relationships[:10]: print(f'  {r.relation} confidence={r.confidence:.0%} basis={"; ".join(r.basis)}')

if __name__=='__main__': main()
