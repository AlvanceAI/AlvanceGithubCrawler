#!/usr/bin/env bash
set -euo pipefail
base_commit=89f5bdae3200527c26b3e0efadf0da105437f1b1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
