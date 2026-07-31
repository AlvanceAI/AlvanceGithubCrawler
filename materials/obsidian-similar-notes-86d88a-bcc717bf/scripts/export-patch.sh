#!/usr/bin/env bash
set -euo pipefail
base_commit=bcc717bf9de70c29aeb14abc3ba83c5bcddd4323
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
