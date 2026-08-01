#!/usr/bin/env bash
set -euo pipefail
base_commit=9eb5b8fdc1e57adb729093e632c281850eb860cc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
