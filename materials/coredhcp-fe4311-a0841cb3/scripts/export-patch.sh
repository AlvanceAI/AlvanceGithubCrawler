#!/usr/bin/env bash
set -euo pipefail
base_commit=a0841cb3038f63e3f93e813648cea8641a3bc5c0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
