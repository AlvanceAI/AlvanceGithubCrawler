#!/usr/bin/env bash
set -euo pipefail
base_commit=268615a5c27dc40e5c22454c07b44d5c50410da0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
