#!/usr/bin/env bash
set -euo pipefail
base_commit=85293e3e2b88f4d2ce330d956b139cf628aa1e82
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
