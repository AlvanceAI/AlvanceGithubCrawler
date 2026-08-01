#!/usr/bin/env bash
set -euo pipefail
base_commit=2151def3553e5521ff8b3e2fea837561c57255f9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
