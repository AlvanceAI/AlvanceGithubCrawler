#!/usr/bin/env bash
set -euo pipefail
base_commit=43f72e275f6cf2deb94ea40f179e393e75cd6000
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
