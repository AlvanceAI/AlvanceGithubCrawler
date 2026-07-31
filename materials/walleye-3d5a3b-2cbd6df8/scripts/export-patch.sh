#!/usr/bin/env bash
set -euo pipefail
base_commit=2cbd6df821e306f3c04d5af9e98b8650cdcb6d79
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
