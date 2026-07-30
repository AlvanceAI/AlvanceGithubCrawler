#!/usr/bin/env bash
set -euo pipefail
base_commit=9a8ed9486637e1fb839f209730eda6c95fd12d88
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
