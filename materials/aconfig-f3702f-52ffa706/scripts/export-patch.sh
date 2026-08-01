#!/usr/bin/env bash
set -euo pipefail
base_commit=52ffa7065e3ea4675ef5da34e8d80920ddcc280a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
