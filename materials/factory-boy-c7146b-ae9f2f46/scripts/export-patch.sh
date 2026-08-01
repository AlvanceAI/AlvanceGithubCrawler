#!/usr/bin/env bash
set -euo pipefail
base_commit=ae9f2f4650afef0bc9b0925de97f618603233ff8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
