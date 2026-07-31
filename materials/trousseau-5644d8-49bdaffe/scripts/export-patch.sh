#!/usr/bin/env bash
set -euo pipefail
base_commit=49bdaffeb22dceffc691eb8f65f098c36624e336
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
