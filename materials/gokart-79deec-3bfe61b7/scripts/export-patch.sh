#!/usr/bin/env bash
set -euo pipefail
base_commit=3bfe61b732ec9b7986ca360ea4907798494cf5eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
