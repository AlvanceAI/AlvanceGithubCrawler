#!/usr/bin/env bash
set -euo pipefail
base_commit=500a1de72fc74a23f946296e2a96d483ee4fc4d5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
