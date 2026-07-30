#!/usr/bin/env bash
set -euo pipefail
base_commit=51ced6986059bac136218c53270f2707987f8aa0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
