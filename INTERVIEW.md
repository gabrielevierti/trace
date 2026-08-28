# TRACE — Interview Brief

## 30-second pitch

> TRACE is a local-first digital evidence correlation engine. I built it around a simple problem: forensic artifacts are often fragmented across browsers, filesystems and system logs. TRACE normalizes those observations, correlates them using explicit rules, and presents the resulting evidence chains as a timeline and graph. The important design decision is that it never hides the reasoning: observed evidence and inferred relationships are kept separate, and every relationship shows its supporting basis and confidence.

## Demo flow

1. Run `trace collect-macos --output CASE-001` on a machine you are authorized to examine.
2. Run `trace verify CASE-001` and show the manifest/integrity result.
3. Analyze a controlled evidence directory with browser artifacts.
4. Open `trace-report.html`.
5. Show the graph.
6. Click a file node.
7. Show the relationship inspector and its basis.
8. Switch to Timeline and Findings.
9. Explain one false-positive boundary and one limitation.

## Technical topics to be ready for

### Why hashes?
SHA-256 gives a deterministic digest of the bytes examined. It supports integrity verification and evidence bookkeeping. It does not prove authorship or user identity.

### Why separate observed and inferred data?
It prevents a correlation rule from being mistaken for a fact. Every inference remains reviewable against its source artifacts.

### Why confidence scores?
They are prioritization scores, not probabilities. A relationship becomes stronger when independent signals agree, such as matching filename, target path and close timestamps.

### Why not use AI?
For a forensic research tool, deterministic and explainable rules make the first version easier to validate. AI can be explored later as an optional review aid, but it should not silently generate investigative conclusions.

### What would you build next?
- More validated macOS artifacts.
- Windows and Android artifact adapters.
- Controlled validation datasets and regression tests.
- A stronger case/evidence package format.
- Signed reports and richer provenance.
- Better graph layouts and filtering.

## Important limitations to state openly

TRACE is not presented as court-ready or as a replacement for validated forensic suites. It is a personal engineering project focused on explainable artifact correlation, evidence integrity and investigator-oriented presentation.
