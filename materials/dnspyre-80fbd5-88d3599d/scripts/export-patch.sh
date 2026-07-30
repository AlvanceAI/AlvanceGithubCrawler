#!/usr/bin/env bash
set -euo pipefail
base_commit=88d3599d10181a30a1f639502429a0ab71351d9d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
