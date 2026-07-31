#!/usr/bin/env bash
set -euo pipefail
base_commit=c083d65c7e002923e7cb98f4e3bdafb105e90f6d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
