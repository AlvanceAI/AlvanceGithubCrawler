#!/usr/bin/env bash
set -euo pipefail
base_commit=2445e4d88a4fdb49206f4a45aa9f3df7b7b6d7bf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
