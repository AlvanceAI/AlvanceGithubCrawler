#!/usr/bin/env bash
set -euo pipefail
base_commit=6aa017643d19ab2718d42f098ee2a65717c2e3b6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
