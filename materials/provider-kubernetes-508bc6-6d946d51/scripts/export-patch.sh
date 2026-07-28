#!/usr/bin/env bash
set -euo pipefail
base_commit=6d946d51b467058a56023bd806977589735749bd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
