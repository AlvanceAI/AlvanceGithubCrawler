#!/usr/bin/env bash
set -euo pipefail
base_commit=d114fff4882cd18e9723907fd0b7d63f3e226033
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
