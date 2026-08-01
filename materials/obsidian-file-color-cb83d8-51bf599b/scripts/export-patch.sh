#!/usr/bin/env bash
set -euo pipefail
base_commit=51bf599b5e68237c433853ef03513e0287f79432
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
