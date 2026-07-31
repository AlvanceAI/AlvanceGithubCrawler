#!/usr/bin/env bash
set -euo pipefail
base_commit=08d7f8dc1c260eb8f0679b8e90e9fc9512f72380
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
