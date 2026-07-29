#!/usr/bin/env bash
set -euo pipefail
base_commit=c7e1f78486b0951ad850f3a65dd831da19f62b92
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
