#!/usr/bin/env bash
set -euo pipefail
base_commit=223fb73e6b48227bf42a97dd64c93c352a992e89
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
