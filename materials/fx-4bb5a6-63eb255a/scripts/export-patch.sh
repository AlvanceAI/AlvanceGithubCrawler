#!/usr/bin/env bash
set -euo pipefail
base_commit=63eb255ad0149ca84c711e89cc85dd6434055405
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
