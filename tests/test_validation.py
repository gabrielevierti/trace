from trace_evidence.model import Artifact
from trace_evidence.correlate import correlate

def test_same_name_far_apart_is_not_high_confidence():
    d=Artifact('d','download','chrome','report.pdf','2026-01-01T00:00:00+00:00')
    f=Artifact('f','file','filesystem','report.pdf','2026-01-02T00:00:00+00:00')
    assert correlate([d,f])[0].confidence < .7

def test_observed_vs_inferred():
    d=Artifact('d','download','chrome','x.pdf')
    f=Artifact('f','file','filesystem','x.pdf')
    r=correlate([d,f])[0]
    assert d.observed and f.observed and r.inferred
