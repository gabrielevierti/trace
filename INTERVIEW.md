# TRACE — interview presentation

## 30-second pitch

> TRACE is a local-first digital evidence correlation engine. I built it to solve a practical problem in forensic analysis: the same activity can leave traces in completely different places. TRACE normalizes those artifacts, preserves their provenance, and creates explainable relationships between them. It deliberately separates observed evidence from inferred correlations, and every inference exposes the rules and evidence that support it.

## Live demo

Use the controlled demo first:

```bash
python3 examples/generate_demo.py
PYTHONPATH=. python -m trace_evidence.cli analyze examples/demo_evidence --case DEMO-001
open trace-report.html
```

Then show a real, authorized directory of your own:

```bash
PYTHONPATH=. python -m trace_evidence.cli analyze ~/Downloads --case LOCAL-001
open trace-report.html
```

If you want browser artifacts and have the relevant local databases:

```bash
PYTHONPATH=. python -m trace_evidence.cli analyze ~/Downloads --chrome --safari --case LOCAL-001
```

## What to demonstrate

1. Open **Evidence Graph** and select an artifact.
2. Show the SHA-256 and filesystem timestamp.
3. Show a relationship and expand its correlation basis.
4. Open **Timeline** to show the same artifacts chronologically.
5. Open **Findings** and explain that indicators are deliberately conservative.
6. Demonstrate evidence integrity with `trace manifest` and `trace verify`.

## Good technical questions to expect

### Why not just use an existing forensic suite?

TRACE is not intended to replace established suites. It is a focused research project demonstrating artifact normalization, provenance, deterministic correlation and explainable reporting. The interesting engineering problem is the correlation layer.

### Why confidence scores?

A filename match alone is weak evidence. A filename plus a matching path and close timestamp is stronger. The score communicates the strength of the correlation without pretending that a heuristic is proof.

### Why separate observed and inferred data?

Forensic analysis must preserve the distinction between what the source artifact actually records and what an analyst infers from multiple artifacts. TRACE makes that distinction explicit in its data model and report UI.

### Why SHA-256 manifests?

The manifest provides a simple integrity check: later verification can identify evidence that is missing or has changed since the manifest was created. It is not a replacement for a complete acquisition/chain-of-custody procedure.

### What would you build next?

- More macOS artifact parsers, with version-specific schemas.
- Windows Registry/Event Log/Prefetch parsers.
- Pluggable artifact parser interface.
- Stronger temporal and hash-based correlation rules.
- Case packages with acquisition metadata and analyst notes.
- Automated parser validation against known-ground-truth datasets.
- A richer graph layout and evidence filtering.

## Important wording

Call TRACE a **research/portfolio forensic tool**. Do not describe it as validated, court-ready, or a replacement for professional forensic software. Do not claim that an indicator proves malicious activity or attribution.
