#!/usr/bin/env bash
set -euo pipefail
base_commit=7a706bee8b258b548cb979c7321c1ba0cf8413e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
