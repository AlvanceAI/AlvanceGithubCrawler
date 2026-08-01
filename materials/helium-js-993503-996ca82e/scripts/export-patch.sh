#!/usr/bin/env bash
set -euo pipefail
base_commit=996ca82e25cc543d4e0a73d0e41442eb706b2c8c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
