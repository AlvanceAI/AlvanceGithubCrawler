#!/usr/bin/env bash
set -euo pipefail
base_commit=1bd51aaedac8e425e21ecfb1941ecf212304014b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
