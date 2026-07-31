#!/usr/bin/env bash
set -euo pipefail
base_commit=d97d1eb0a904546ed059b0a33dd5d4aa3e199c9a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
