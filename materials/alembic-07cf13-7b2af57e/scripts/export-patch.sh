#!/usr/bin/env bash
set -euo pipefail
base_commit=7b2af57eba318a712b7b4f79c7bc6b3669055636
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
