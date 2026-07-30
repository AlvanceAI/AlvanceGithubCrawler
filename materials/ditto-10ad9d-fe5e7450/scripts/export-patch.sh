#!/usr/bin/env bash
set -euo pipefail
base_commit=fe5e74503cf7825cd24049398eabc804d26cb886
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
