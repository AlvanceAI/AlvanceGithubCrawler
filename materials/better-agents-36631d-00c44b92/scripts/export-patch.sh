#!/usr/bin/env bash
set -euo pipefail
base_commit=00c44b92fafc245fa051a34910128e36e85aad07
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
