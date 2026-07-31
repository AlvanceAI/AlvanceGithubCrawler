#!/usr/bin/env bash
set -euo pipefail
base_commit=62bfce68b934aab205bd60beb136112a5bfa1da1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
