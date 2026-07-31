#!/usr/bin/env bash
set -euo pipefail
base_commit=b48ebe9a1d1b186f53cd5ec83c978a4758facf76
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
