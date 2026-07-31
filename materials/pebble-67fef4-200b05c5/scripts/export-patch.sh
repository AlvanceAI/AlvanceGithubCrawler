#!/usr/bin/env bash
set -euo pipefail
base_commit=200b05c58ec8d6906f9da99a9480deb00c51fb24
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
