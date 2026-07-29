#!/usr/bin/env bash
set -euo pipefail
base_commit=6c439f858dd5eea092fbf641831807b202125f84
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
