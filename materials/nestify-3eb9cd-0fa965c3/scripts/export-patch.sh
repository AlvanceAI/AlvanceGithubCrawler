#!/usr/bin/env bash
set -euo pipefail
base_commit=0fa965c3a97746b1b8d9d20c246f9a75ca37e24b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
