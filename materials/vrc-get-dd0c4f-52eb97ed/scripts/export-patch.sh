#!/usr/bin/env bash
set -euo pipefail
base_commit=52eb97eddbf27b03772e0137adb74fc7122d8ced
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
