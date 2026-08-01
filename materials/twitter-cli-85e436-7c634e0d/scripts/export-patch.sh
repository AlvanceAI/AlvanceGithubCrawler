#!/usr/bin/env bash
set -euo pipefail
base_commit=7c634e0d396b1e7af9f63315b414925fe4f29ae7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
