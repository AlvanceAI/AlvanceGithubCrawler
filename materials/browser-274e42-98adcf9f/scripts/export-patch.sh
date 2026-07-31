#!/usr/bin/env bash
set -euo pipefail
base_commit=98adcf9f33a503e68373e18590d68451387ed4dd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
