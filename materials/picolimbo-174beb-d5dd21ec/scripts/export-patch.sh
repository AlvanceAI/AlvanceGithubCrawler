#!/usr/bin/env bash
set -euo pipefail
base_commit=d5dd21ecbe33290e757f65d5d80eb1e6fe6772a1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
