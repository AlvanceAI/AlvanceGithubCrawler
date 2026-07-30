#!/usr/bin/env bash
set -euo pipefail
base_commit=5c20635a24a1afa48c167775081015cae6321a4f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
