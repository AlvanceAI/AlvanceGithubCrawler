#!/usr/bin/env bash
set -euo pipefail
base_commit=0e3de1ede38f595224be03d9457826749b1ae546
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
