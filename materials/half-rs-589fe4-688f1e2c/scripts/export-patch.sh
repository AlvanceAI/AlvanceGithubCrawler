#!/usr/bin/env bash
set -euo pipefail
base_commit=688f1e2c2a541186802b6b0fe0e6761cdb507428
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
