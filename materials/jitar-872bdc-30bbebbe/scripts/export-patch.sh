#!/usr/bin/env bash
set -euo pipefail
base_commit=30bbebbeb3644f298dc3e78dbb5b4eb02c2a80e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
