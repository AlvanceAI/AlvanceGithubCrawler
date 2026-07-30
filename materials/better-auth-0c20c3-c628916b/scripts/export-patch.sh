#!/usr/bin/env bash
set -euo pipefail
base_commit=c628916b451a6b4cff0f5464f134475464b1a6da
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
