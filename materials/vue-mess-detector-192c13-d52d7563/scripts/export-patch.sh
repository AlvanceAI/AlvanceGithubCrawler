#!/usr/bin/env bash
set -euo pipefail
base_commit=d52d75632bd49bddf4a090912b7b21a508f6a537
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
