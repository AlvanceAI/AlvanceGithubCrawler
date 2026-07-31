#!/usr/bin/env bash
set -euo pipefail
base_commit=0767a458e50fa1f7ae203b73e50298ab201c80bb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
