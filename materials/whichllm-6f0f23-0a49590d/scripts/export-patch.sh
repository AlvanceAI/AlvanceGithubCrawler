#!/usr/bin/env bash
set -euo pipefail
base_commit=0a49590df0df7bbdda250fad064e7ab8688e2e92
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
