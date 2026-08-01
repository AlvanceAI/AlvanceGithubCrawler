#!/usr/bin/env bash
set -euo pipefail
base_commit=9eb8b8fd0b86567b5f7dc19362ba760c9c52666c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
