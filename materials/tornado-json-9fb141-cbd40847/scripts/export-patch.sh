#!/usr/bin/env bash
set -euo pipefail
base_commit=cbd408471aade7a8acb9f784721a7e0a115d4bfb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
