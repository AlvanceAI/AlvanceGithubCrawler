#!/usr/bin/env bash
set -euo pipefail
base_commit=240d4bcd3e207c7ed1cebd9908be41150c3ea1ab
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
