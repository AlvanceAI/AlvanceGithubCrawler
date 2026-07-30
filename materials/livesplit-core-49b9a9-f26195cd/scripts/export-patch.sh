#!/usr/bin/env bash
set -euo pipefail
base_commit=f26195cd80e71e3be1a4cec4378180109b910410
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
