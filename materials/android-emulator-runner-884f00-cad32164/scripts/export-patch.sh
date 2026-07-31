#!/usr/bin/env bash
set -euo pipefail
base_commit=cad321644df6d8cf1985a42767272ff068adb9cb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
