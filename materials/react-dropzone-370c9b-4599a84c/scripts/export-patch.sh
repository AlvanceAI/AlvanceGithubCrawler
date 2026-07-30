#!/usr/bin/env bash
set -euo pipefail
base_commit=4599a84cfe483aa5ac38753882cfee9639fb35ba
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
