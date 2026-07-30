#!/usr/bin/env bash
set -euo pipefail
base_commit=fcc55a694c62bd516ba00c2e303c178472b65f41
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
