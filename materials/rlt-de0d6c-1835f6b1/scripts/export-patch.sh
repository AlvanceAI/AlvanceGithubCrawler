#!/usr/bin/env bash
set -euo pipefail
base_commit=1835f6b16668dd688e6b7ba6595286098c055a39
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
