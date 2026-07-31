#!/usr/bin/env bash
set -euo pipefail
base_commit=16419356370fdbe6f006c6d4521bdb2c660f9411
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
