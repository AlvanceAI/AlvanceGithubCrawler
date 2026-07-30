#!/usr/bin/env bash
set -euo pipefail
base_commit=4176778b8febe685f6888528e70f381bf1070fd3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
