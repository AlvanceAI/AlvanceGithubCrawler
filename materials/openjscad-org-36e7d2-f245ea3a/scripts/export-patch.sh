#!/usr/bin/env bash
set -euo pipefail
base_commit=f245ea3a5072024b789f276c6fb9ce6c3eb3fd0d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
