#!/usr/bin/env bash
set -euo pipefail
base_commit=3079d9a89d178e7eb2651bcae73e889c42683be1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
