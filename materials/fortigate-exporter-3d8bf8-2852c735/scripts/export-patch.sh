#!/usr/bin/env bash
set -euo pipefail
base_commit=2852c735b4b3af44321e676d76d9c3bed4a7efa5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
