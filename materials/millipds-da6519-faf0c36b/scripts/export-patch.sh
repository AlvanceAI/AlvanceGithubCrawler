#!/usr/bin/env bash
set -euo pipefail
base_commit=faf0c36ba65183eba47c1d4f50d084aa11f4ce95
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
