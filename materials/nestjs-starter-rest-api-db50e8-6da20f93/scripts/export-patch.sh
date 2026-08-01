#!/usr/bin/env bash
set -euo pipefail
base_commit=6da20f930269d68c1417f6b1992fd820172ce013
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
