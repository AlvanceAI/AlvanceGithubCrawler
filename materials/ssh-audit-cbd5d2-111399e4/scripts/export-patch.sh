#!/usr/bin/env bash
set -euo pipefail
base_commit=111399e4319a7297c9edd075725048c5638dbceb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
