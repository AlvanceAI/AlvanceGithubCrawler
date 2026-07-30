#!/usr/bin/env bash
set -euo pipefail
base_commit=b9de7fd88f009e9f65f2421370f0d5fbd4b1be5e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
