#!/usr/bin/env bash
set -euo pipefail
base_commit=79e2ba6f0db7776578bd7de67948a5eb53cf8a75
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
