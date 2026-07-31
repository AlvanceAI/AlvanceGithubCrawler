#!/usr/bin/env bash
set -euo pipefail
base_commit=44e3b535e15c65a04c85e7be057b548aca7dfb90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
