#!/usr/bin/env bash
set -euo pipefail
base_commit=c556c9a209fb40fb2a1d68a90ed95ad04b592cdd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
