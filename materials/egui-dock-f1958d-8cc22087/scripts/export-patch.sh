#!/usr/bin/env bash
set -euo pipefail
base_commit=8cc22087c729a10445a8f4727164d53f6a5f479a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
