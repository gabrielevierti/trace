from pathlib import Path
import os
import tempfile, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trace_evidence.parsers.filesystem import scan
from trace_evidence.model import Artifact
from trace_evidence.correlate import correlate
from trace_evidence.analyzers import analyze_files
from trace_evidence.report import write_json,write_html
root=Path(__file__).parent/'demo_evidence'; root.mkdir(exist_ok=True)
(root/'invoice.pdf').write_bytes(b'%PDF-1.7\n% demo evidence\n/JavaScript\n'); os.utime(root/'invoice.pdf',(1787911200,1787911200))
arts=scan(root)
arts.append(Artifact('demo:visit','browser_visit','chrome','example.test','2026-08-28T09:59:40+00:00',metadata={'url':'https://example.test/invoice.pdf'}))
arts.append(Artifact('demo:download','download','chrome','invoice.pdf','2026-08-28T10:00:00+00:00',str(root/'invoice.pdf'),metadata={'url':'https://example.test/invoice.pdf'}))
rel=correlate(arts); findings=analyze_files(arts)
case={'case_id':'DEMO-001','evidence_path':str(root),'analysis_version':'1.0.0'}
write_json(Path(__file__).parent/'demo-report.json',arts,rel,findings,case)
write_html(Path(__file__).parent/'demo-report.html',arts,rel,findings,case)
print('Generated examples/demo-report.html')
