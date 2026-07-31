#!/usr/bin/env bash
set -euo pipefail
base_commit=bc2b7ceee4b4d4c9ba5ec2451afdd43462f0b188
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
