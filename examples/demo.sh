#!/usr/bin/env bash
set -e
mkdir -p /tmp/trace-demo
printf 'TRACE demo evidence\n' > /tmp/trace-demo/report.pdf
trace analyze /tmp/trace-demo --output /tmp/trace-demo/report.html
