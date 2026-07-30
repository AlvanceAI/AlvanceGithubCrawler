#!/usr/bin/env bash
set -euo pipefail
base_commit=07b51e8268c6650130cb005647e6035aec317132
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
