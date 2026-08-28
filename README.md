# TRACE

**Digital Evidence Correlation Engine**

TRACE is a local-first research tool for examining real digital artifacts and building **explainable relationships** between them. It is designed as a portfolio/research project for digital forensics: observed evidence is kept separate from inferred correlations, and every correlation exposes the evidence used to derive it.

## What it does

- Hashes files with SHA-256 and records filesystem timestamps.
- Detects file types from content signatures rather than trusting extensions.
- Calculates Shannon entropy and extracts basic metadata indicators.
- Parses Chrome History and Downloads databases.
- Parses common Safari history databases when the local schema permits it.
- Normalizes artifacts into one timeline-friendly model.
- Correlates downloads, browser visits and filesystem artifacts using transparent rules.
- Produces an interactive standalone HTML Evidence Graph + Inspector.
- Exports machine-readable JSON.
- Creates SHA-256 integrity manifests and can verify later whether evidence files changed.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
trace analyze ./evidence --chrome --safari --case CASE-001
open trace-report.html
```

If browser databases are copied from another location:

```bash
trace analyze ./evidence --chrome /path/to/History --safari /path/to/History.db
```

Create an integrity manifest:

```bash
mkdir -p CASE-001
touch CASE-001/placeholder
trace manifest CASE-001 ./evidence/file.pdf ./evidence/image.jpg
trace verify CASE-001/manifest.json
```

## Architecture

```text
                 REAL EVIDENCE
                      |
          +-----------+-----------+
          |                       |
     Artifact parsers       File analysis
          |                       |
          +-----------+-----------+
                      v
                Artifact model
                      |
                      v
              Correlation engine
                      |
             +--------+--------+
             |                 |
          Timeline        Evidence Graph
             |                 |
             +--------+--------+
                      v
             HTML / JSON report
```

## Forensic design principles

**Observed ≠ inferred.** A browser record or filesystem timestamp is an observation. A relationship such as `preceded_download` is an inference and includes its confidence and basis.

**Explainability.** Correlation rules are deterministic and visible. TRACE does not claim attribution or guilt.

**Integrity.** Evidence manifests store SHA-256 hashes so a later verification can detect missing or modified files.

**Local-first.** The core analysis does not upload evidence to a server.

## Scope and limitations

TRACE is a research/portfolio tool, not a validated forensic product and not a substitute for established forensic suites or acquisition procedures. It should be used on evidence you are authorized to examine. Browser database schemas and operating-system artifacts change between releases; parsers therefore fail conservatively rather than pretending an unsupported artifact is valid.