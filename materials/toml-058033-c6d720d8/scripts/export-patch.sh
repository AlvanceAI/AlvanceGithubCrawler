#!/usr/bin/env bash
set -euo pipefail
base_commit=c6d720d83547bb8d7afb067ba9df8bad0323e2d1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
