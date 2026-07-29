#!/usr/bin/env bash
set -euo pipefail
base_commit=be178a7479d5a472d6e3fce791c20bf098e1451e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
