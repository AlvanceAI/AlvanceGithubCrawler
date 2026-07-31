#!/usr/bin/env bash
set -euo pipefail
base_commit=fd7dac646eea56c9ac9c1d36893e611de855c21e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
