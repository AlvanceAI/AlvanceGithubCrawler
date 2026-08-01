#!/usr/bin/env bash
set -euo pipefail
base_commit=ad133ab60056575359f9869c03e906c33764a003
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
