#!/usr/bin/env bash
set -euo pipefail
base_commit=84686bb66ba1790dcadc7513c36d233969ea4518
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
