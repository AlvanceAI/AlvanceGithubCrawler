#!/usr/bin/env bash
set -euo pipefail
base_commit=aacf810e7ae5bb1c546fbc646ad3568dd7df87d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
