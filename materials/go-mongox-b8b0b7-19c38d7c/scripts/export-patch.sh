#!/usr/bin/env bash
set -euo pipefail
base_commit=19c38d7c2edcaf14e958a1e086d1f5e40363c924
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
