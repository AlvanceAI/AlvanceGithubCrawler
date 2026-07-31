#!/usr/bin/env bash
set -euo pipefail
base_commit=8fda6a636efbc14f236209cd98c7aa442d218d27
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
