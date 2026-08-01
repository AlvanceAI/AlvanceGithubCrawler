#!/usr/bin/env bash
set -euo pipefail
base_commit=d18b8e9f59bd706eb16c347693ed82c670d60d1b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
