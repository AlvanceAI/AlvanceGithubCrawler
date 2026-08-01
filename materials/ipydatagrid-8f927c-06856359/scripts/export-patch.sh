#!/usr/bin/env bash
set -euo pipefail
base_commit=0685635938395866ba3f9b62bcca8fa4c973d7d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
