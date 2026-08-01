#!/usr/bin/env bash
set -euo pipefail
base_commit=22073eacc4780b835830b9987de42840351bc8e4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
