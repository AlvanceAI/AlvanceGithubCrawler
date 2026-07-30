#!/usr/bin/env bash
set -euo pipefail
base_commit=b766be144d675b31f9b8effdf9cfc625d7db740f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
