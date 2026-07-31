#!/usr/bin/env bash
set -euo pipefail
base_commit=8cad765426016ff935c7cd9f8045882289b73748
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
