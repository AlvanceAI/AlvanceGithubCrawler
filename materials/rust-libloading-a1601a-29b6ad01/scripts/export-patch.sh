#!/usr/bin/env bash
set -euo pipefail
base_commit=29b6ad019067e90399593275a1c53d2343d2e6b1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
