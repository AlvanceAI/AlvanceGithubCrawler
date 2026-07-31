#!/usr/bin/env bash
set -euo pipefail
base_commit=7df532dc29f6bbf4204d62796f4ff537594f5097
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
