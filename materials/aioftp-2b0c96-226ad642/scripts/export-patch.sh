#!/usr/bin/env bash
set -euo pipefail
base_commit=226ad64264c5dd7e93a56fe92544b7cf0cc5da50
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
