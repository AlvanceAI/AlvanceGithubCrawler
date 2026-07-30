#!/usr/bin/env bash
set -euo pipefail
base_commit=4a876cf945e60a7834d05f49070ae34662225686
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
