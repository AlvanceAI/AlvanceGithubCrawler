#!/usr/bin/env bash
set -euo pipefail
base_commit=bc279ad068f571fa211db9e2d90555e1d0735df4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
