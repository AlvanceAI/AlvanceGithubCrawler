#!/usr/bin/env bash
set -euo pipefail
base_commit=515a0142f99172516fd2b37fda86bd9e00541e0a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
