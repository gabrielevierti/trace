from trace_evidence.model import Artifact
from trace_evidence.correlate import correlate

def test_download_file_correlation():
    d=Artifact('d','download','chrome','report.pdf','2026-08-28T10:00:00+00:00','/tmp/report.pdf',None,{'url':'https://example.test/report.pdf'})
    f=Artifact('f','file','filesystem','report.pdf','2026-08-28T10:00:02+00:00','/tmp/report.pdf','abc',{})
    v=Artifact('v','browser_visit','chrome','Report','2026-08-28T09:59:50+00:00',None,None,{'url':'https://example.test/report.pdf'})
    rs=correlate([d,f,v]); assert any(r.relation=='downloaded_as' and r.confidence>.9 for r in rs); assert any(r.relation=='preceded_download' for r in rs)
