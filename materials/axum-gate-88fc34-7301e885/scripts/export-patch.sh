#!/usr/bin/env bash
set -euo pipefail
base_commit=7301e885ee1c3367e6d310afc10fa20cd594e3e4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
