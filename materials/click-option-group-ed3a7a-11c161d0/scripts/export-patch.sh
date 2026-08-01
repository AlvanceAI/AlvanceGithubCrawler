#!/usr/bin/env bash
set -euo pipefail
base_commit=11c161d0f66768510f45459a38e673a00b1918d8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
