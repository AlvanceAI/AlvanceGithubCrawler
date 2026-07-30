#!/usr/bin/env bash
set -euo pipefail
base_commit=3c81aac2e1b48125efdf0c996fbbb9c72c06ae50
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
