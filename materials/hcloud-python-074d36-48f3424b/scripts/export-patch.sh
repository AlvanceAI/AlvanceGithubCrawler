#!/usr/bin/env bash
set -euo pipefail
base_commit=48f3424b49ece33652cd8ca7163e857ca3fecbb9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
