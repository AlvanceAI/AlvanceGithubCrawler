#!/usr/bin/env bash
set -euo pipefail
base_commit=fcc8ed889845ba094b2b002c9c2a3147fb849374
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
