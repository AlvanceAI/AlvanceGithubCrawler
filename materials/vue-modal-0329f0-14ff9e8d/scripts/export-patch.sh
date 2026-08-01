#!/usr/bin/env bash
set -euo pipefail
base_commit=14ff9e8d926c09050d8d0e3ce1c1c400b4560fb1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
