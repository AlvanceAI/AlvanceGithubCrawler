#!/usr/bin/env bash
set -euo pipefail
base_commit=d0ff901fb14ebc67ed91a67232bc0a923957fcd0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
