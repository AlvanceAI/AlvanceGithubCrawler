#!/usr/bin/env bash
set -euo pipefail
base_commit=2224255c4acc594d734cef0bbc83360452a67983
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
