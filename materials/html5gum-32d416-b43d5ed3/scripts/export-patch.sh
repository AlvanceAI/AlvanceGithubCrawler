#!/usr/bin/env bash
set -euo pipefail
base_commit=b43d5ed3460f96d7fa9783b4d76a21e6389c3bf0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
