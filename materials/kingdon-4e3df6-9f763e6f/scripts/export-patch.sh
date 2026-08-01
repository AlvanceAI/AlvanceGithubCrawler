#!/usr/bin/env bash
set -euo pipefail
base_commit=9f763e6f859e4ac6a0fed5d8bcfaea8881d812c0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
