#!/usr/bin/env bash
set -euo pipefail
base_commit=6860573a014ca6361adb77b1c5b8e5fcfab44216
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
