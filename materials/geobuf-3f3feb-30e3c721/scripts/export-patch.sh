#!/usr/bin/env bash
set -euo pipefail
base_commit=30e3c72136f1785ebd2d6e88a472f7de9e15806e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
