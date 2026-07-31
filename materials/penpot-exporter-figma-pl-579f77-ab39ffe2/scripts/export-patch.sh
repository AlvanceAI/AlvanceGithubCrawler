#!/usr/bin/env bash
set -euo pipefail
base_commit=ab39ffe206bacfae767a58cf45ec92a26ec9eb1e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
