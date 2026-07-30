#!/usr/bin/env bash
set -euo pipefail
base_commit=a75a1573f2113e10c56d6cc309d3138b9bed1dc6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
