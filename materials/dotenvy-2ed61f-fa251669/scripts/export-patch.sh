#!/usr/bin/env bash
set -euo pipefail
base_commit=fa25166994d6978bd2e002f0ed190c0c39674ebe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
