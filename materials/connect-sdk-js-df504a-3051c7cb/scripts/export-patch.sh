#!/usr/bin/env bash
set -euo pipefail
base_commit=3051c7cb055958d62fa8a36bf3cc8b7f4a30512c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
