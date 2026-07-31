#!/usr/bin/env bash
set -euo pipefail
base_commit=939affd3acc60395bb34749cabb80cc19bcd20eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
