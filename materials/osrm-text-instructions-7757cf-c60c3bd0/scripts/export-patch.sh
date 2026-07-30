#!/usr/bin/env bash
set -euo pipefail
base_commit=c60c3bd0d8ad9441e835a7bf5729cd20ed99f2e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
