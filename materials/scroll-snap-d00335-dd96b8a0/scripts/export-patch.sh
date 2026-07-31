#!/usr/bin/env bash
set -euo pipefail
base_commit=dd96b8a0c1244d3930be4390e68d076f497d9fb4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
