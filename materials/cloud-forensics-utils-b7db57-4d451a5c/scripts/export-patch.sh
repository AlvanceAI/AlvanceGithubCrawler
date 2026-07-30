#!/usr/bin/env bash
set -euo pipefail
base_commit=4d451a5c205d256be1ba5a3bbf515a8f54a4f295
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
