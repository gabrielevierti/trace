# TRACE

**Digital Evidence Correlation Engine**

TRACE is a local-first, explainable digital-forensics research tool. It parses real filesystem and browser artifacts, normalizes them into a common evidence model, and creates explicit relationships between artifacts. It deliberately separates **observed evidence** from **inferred relationships**.

## What it does

- SHA-256 hashing for files
- Recursive filesystem artifact collection
- Chrome download-history parsing
- Safari history parsing
- Explainable correlation rules
- Confidence scoring
- Interactive standalone HTML evidence graph
- Evidence inspector showing the exact basis for every inferred relationship
- JSON export suitable for further analysis

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
trace analyze ./evidence --chrome --safari
open trace-report.html
```

Use a dedicated test/evidence directory first. TRACE is a research/educational tool, not a validated forensic acquisition or courtroom-grade examination suite. Preserve original evidence separately and work from copies.

## Design principle

TRACE distinguishes:

**Observed** — an artifact directly parsed from a source.

**Inferred** — a relationship proposed from explicit, inspectable rules. Every relationship contains its basis and confidence score.

## License

MIT
