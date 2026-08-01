#!/usr/bin/env bash
set -euo pipefail
base_commit=79de0db33ac28f802a64f9578b0dd83598ca1fed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
