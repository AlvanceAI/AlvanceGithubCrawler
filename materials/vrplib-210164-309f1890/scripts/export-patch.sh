#!/usr/bin/env bash
set -euo pipefail
base_commit=309f18900f54a91ec3aeaf8b840c0db351aa8c5d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
