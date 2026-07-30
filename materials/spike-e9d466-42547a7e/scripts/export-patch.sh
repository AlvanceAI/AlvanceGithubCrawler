#!/usr/bin/env bash
set -euo pipefail
base_commit=42547a7e5a0099e47c95046889030b895c0ec430
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
