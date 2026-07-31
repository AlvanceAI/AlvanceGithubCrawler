#!/usr/bin/env bash
set -euo pipefail
base_commit=47d4bf94104c0de70e26075e0f2c991b97af64ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
