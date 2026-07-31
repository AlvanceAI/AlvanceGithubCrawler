#!/usr/bin/env bash
set -euo pipefail
base_commit=fd7af690654dc096b073ddbdcd49c76303190ac7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
