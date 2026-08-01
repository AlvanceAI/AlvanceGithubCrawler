#!/usr/bin/env bash
set -euo pipefail
base_commit=ed40ec3bbef03bb08938ad1a74d459b0d1ab81f7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
