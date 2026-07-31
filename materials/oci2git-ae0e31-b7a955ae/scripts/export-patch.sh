#!/usr/bin/env bash
set -euo pipefail
base_commit=b7a955ae5e6cf7819b2b8679a7ea670d01072420
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
