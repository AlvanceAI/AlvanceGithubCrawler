#!/usr/bin/env bash
set -euo pipefail
base_commit=770c6cec2e8aa08d7f6c164b2706f749d4398f49
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
