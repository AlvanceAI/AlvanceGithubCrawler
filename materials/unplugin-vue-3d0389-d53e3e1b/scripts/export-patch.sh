#!/usr/bin/env bash
set -euo pipefail
base_commit=d53e3e1b456a6ebafd75434b961c30283ffdcaaf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
