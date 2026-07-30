#!/usr/bin/env bash
set -euo pipefail
base_commit=1a0ddb1efec8b5c2ecac6431c75da5eebc469ed0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
