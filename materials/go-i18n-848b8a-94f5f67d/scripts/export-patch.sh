#!/usr/bin/env bash
set -euo pipefail
base_commit=94f5f67df91a966340ef80ce401fa0b4b94b8b4e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
