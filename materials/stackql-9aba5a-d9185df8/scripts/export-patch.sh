#!/usr/bin/env bash
set -euo pipefail
base_commit=d9185df8f84fedf6b1a4e22a54f46eddb651f5bb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
