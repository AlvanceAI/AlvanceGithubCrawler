#!/usr/bin/env bash
set -euo pipefail
base_commit=29ee27c9b5fb2ab451d79b2d62b83e44c4dff58f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
