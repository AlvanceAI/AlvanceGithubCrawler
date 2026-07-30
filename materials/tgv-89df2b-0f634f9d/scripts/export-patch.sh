#!/usr/bin/env bash
set -euo pipefail
base_commit=0f634f9de23c47e6724f326bfe4568a381dbaf57
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
