#!/usr/bin/env bash
set -euo pipefail
base_commit=10965cddfa169679511f176cfe67dd0189dc935f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
