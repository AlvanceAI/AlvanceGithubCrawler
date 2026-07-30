#!/usr/bin/env bash
set -euo pipefail
base_commit=b00987e194e5c2c2ab51e22ab1c97454f3e42681
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
