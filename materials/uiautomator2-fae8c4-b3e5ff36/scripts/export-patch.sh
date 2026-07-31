#!/usr/bin/env bash
set -euo pipefail
base_commit=b3e5ff36b04b0f30c132288b554e82b65957057f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
