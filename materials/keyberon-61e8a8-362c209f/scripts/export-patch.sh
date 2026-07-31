#!/usr/bin/env bash
set -euo pipefail
base_commit=362c209f729d05505abb1984a0ddb321ec9ebf53
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
