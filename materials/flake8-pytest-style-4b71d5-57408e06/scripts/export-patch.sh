#!/usr/bin/env bash
set -euo pipefail
base_commit=57408e0668c5c0fa57969bbed1806961153540ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
