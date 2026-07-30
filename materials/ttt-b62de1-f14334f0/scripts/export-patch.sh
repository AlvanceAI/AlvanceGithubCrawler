#!/usr/bin/env bash
set -euo pipefail
base_commit=f14334f0942fc85bf03822758525eb7bedc8aa36
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
