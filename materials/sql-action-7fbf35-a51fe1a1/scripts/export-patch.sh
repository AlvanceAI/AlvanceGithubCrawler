#!/usr/bin/env bash
set -euo pipefail
base_commit=a51fe1a149c6ec1720555441e70c1d83dddd99b0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
