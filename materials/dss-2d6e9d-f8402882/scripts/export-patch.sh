#!/usr/bin/env bash
set -euo pipefail
base_commit=f84028826a587ea7ed28f1cf92c0ec8221404291
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
