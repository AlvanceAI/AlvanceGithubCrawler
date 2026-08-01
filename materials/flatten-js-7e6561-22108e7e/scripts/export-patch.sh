#!/usr/bin/env bash
set -euo pipefail
base_commit=22108e7e238dc5a5f4bab30a49703b96190bd0ec
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
