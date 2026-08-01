#!/usr/bin/env bash
set -euo pipefail
base_commit=b6fe3562c95f200b327e865fc5b33df8744ea0ac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
