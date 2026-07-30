#!/usr/bin/env bash
set -euo pipefail
base_commit=2e3f100aa8bf27818545a7024fb5e743cd844273
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
