#!/usr/bin/env bash
set -euo pipefail
base_commit=abeae765dd546dfff60b278f0757dcc71beb8ab1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
