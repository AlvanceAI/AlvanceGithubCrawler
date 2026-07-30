#!/usr/bin/env bash
set -euo pipefail
base_commit=c1991f8fc3eb8774907f0cffb93792f59079cd7a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
