#!/usr/bin/env bash
set -euo pipefail
base_commit=6ff8fb77ee3948b4a025e1a49bf959750e7bab9d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
