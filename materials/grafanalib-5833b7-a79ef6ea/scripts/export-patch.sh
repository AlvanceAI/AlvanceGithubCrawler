#!/usr/bin/env bash
set -euo pipefail
base_commit=a79ef6eaf143ae1fb0fedb8f655a2e9aa7c1c5d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
