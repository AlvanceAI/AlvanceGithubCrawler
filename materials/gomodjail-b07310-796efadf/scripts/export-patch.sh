#!/usr/bin/env bash
set -euo pipefail
base_commit=796efadf08ddd9bb913a9c48960767b43ab61e80
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
