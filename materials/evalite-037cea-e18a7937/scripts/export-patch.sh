#!/usr/bin/env bash
set -euo pipefail
base_commit=e18a793789400b9292f92465d1084344340aef9b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
