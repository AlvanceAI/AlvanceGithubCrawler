#!/usr/bin/env bash
set -euo pipefail
base_commit=54d464d472775c63a1855d326fff692db92aa0b8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
