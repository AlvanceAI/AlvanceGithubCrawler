#!/usr/bin/env bash
set -euo pipefail
base_commit=0c04e85a529e88e1c1461bfc600cb5787c7f96f6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
