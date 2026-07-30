#!/usr/bin/env bash
set -euo pipefail
base_commit=5d6e7377d1d811003b7225750fff3a17c16295f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
