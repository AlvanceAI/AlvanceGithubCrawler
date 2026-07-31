#!/usr/bin/env bash
set -euo pipefail
base_commit=b08a906e6c19738900c7b3b0c699b249b456d07e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
