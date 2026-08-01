#!/usr/bin/env bash
set -euo pipefail
base_commit=1f9cbbce78a93f96a35abf2db5425361e2abf142
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
