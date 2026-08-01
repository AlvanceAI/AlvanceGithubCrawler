#!/usr/bin/env bash
set -euo pipefail
base_commit=72331ff5d13a8d4d1f11256a7b554dd0d69d7014
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
