#!/usr/bin/env bash
set -euo pipefail
base_commit=b2f1d9b79b1d264a5747f46707d72b1aa40a02ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
