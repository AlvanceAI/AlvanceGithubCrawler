#!/usr/bin/env bash
set -euo pipefail
base_commit=d25beede911d59a571382c6821cb8e7a7c27850a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
