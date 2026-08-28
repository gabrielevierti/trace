#!/bin/sh
set -e
python examples/generate_demo.py
trace analyze examples/demo_evidence --case DEMO-001
printf '\nOpen trace-report.html in your browser.\n'
