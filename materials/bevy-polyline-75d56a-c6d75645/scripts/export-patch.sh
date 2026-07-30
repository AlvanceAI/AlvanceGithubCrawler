#!/usr/bin/env bash
set -euo pipefail
base_commit=c6d756450adff298182f0ac45ce5d81927990c70
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
