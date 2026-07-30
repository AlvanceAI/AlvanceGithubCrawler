#!/usr/bin/env bash
set -euo pipefail
base_commit=5280e7fcc50868cf940c7f16bdb8cae1201adb3f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
