#!/usr/bin/env bash
set -euo pipefail
base_commit=4d7af4d3f13f7651fb538328b6d57eacdfc4f8d7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
