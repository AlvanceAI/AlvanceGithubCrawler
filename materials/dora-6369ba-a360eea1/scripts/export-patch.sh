#!/usr/bin/env bash
set -euo pipefail
base_commit=a360eea184266d756ee718510e7370cd27dffb3b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
