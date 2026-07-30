#!/usr/bin/env bash
set -euo pipefail
base_commit=44050a6fd1aa88af258fe155b43beea59fe6bf4d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
