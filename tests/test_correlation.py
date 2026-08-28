from trace_evidence.model import Artifact
from trace_evidence.correlate import correlate


def test_download_file_correlation():
    artifacts=[
        Artifact('d','download','chrome','report.pdf','2026-01-01T12:00:00+00:00','/tmp/report.pdf',metadata={'url':'https://example.test/report.pdf'}),
        Artifact('f','file','filesystem','report.pdf','2026-01-01T12:00:02+00:00','/tmp/report.pdf','abc'),
    ]
    rs=correlate(artifacts)
    assert any(r.relation=='downloaded_as' and r.confidence > .8 for r in rs)
