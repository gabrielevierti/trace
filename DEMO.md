# Five-minute demo

The repository contains a reproducible demo so the project can be shown without touching personal data.

```bash
python3 examples/generate_demo.py
open examples/demo-report.html
```

For a real, authorized macOS dataset:

```bash
trace collect-macos --output CASE-001
trace analyze CASE-001/evidence/macos --case CASE-001 \
  --chrome-path CASE-001/evidence/macos/History \
  --safari-path CASE-001/evidence/macos/History.db \
  --quarantine --quarantine-path CASE-001/evidence/macos/QuarantineEventsV2 \
  --usb-profile CASE-001/evidence/macos/system_profiler_usb.xml \
  --unified-log CASE-001/evidence/macos/unified.log.txt \
  --json CASE-001/reports/report.json \
  --output CASE-001/reports/report.html \
  --pdf CASE-001/reports/report.pdf
open CASE-001/reports/report.html
```
