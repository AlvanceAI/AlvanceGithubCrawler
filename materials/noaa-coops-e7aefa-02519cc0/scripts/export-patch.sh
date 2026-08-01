#!/usr/bin/env bash
set -euo pipefail
base_commit=02519cc0dc516fc8df8e49bf1cf9ecaeb294bd57
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
