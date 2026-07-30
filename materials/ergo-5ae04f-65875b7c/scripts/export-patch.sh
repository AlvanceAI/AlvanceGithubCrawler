#!/usr/bin/env bash
set -euo pipefail
base_commit=65875b7c61c317523da71245045f1a5f0e935e79
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
