#!/usr/bin/env bash
set -euo pipefail
base_commit=72b962f477dc17f7ed41e68a9aea57a3f80a2154
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
