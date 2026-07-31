#!/usr/bin/env bash
set -euo pipefail
base_commit=d56eb651d7757f71fa8143c9a8630f251f894322
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
