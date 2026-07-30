#!/usr/bin/env bash
set -euo pipefail
base_commit=02b6f874525927a501daf8004cae8a30f91723a2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
