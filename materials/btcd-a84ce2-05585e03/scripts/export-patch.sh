#!/usr/bin/env bash
set -euo pipefail
base_commit=05585e037ba0690572208dbc46d121a49cc0c4c9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
