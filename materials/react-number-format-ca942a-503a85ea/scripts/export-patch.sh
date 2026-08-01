#!/usr/bin/env bash
set -euo pipefail
base_commit=503a85ea16c182a114731405f6a504d7e86a5dcb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
