#!/usr/bin/env bash
set -euo pipefail
base_commit=e6cacde5692cf4c914ff2ddb882b124d4bfbc52b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
