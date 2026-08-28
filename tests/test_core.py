from pathlib import Path
from trace_evidence.model import Artifact
from trace_evidence.correlate import correlate
from trace_evidence.util import sha256

def test_hash(tmp_path):
    p=tmp_path/'a.txt'; p.write_text('hello')
    assert len(sha256(p))==64

def test_download_correlation():
    d=Artifact('d','download','chrome','a.pdf','2026-01-01T00:00:00+00:00','/x/a.pdf',metadata={'url':'https://example.test/a.pdf'})
    f=Artifact('f','file','filesystem','a.pdf','2026-01-01T00:00:02+00:00','/x/a.pdf')
    assert correlate([d,f])[0].confidence >= .8
