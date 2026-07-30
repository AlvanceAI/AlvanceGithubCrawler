#!/usr/bin/env bash
set -euo pipefail
base_commit=2dd8ec6b3796d4ae3a455456fa63b22f123e5cab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
