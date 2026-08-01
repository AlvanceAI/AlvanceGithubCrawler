#!/usr/bin/env bash
set -euo pipefail
base_commit=0801afd276f2f7086ae8fecb07a5eac102227b74
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
