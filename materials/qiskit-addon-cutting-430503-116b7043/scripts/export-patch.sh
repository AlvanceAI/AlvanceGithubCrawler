#!/usr/bin/env bash
set -euo pipefail
base_commit=116b7043999a96c7d402e09d3675c53f119a52b0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
