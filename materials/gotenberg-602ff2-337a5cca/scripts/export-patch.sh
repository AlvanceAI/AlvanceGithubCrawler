#!/usr/bin/env bash
set -euo pipefail
base_commit=337a5cca64883f31faa4087b5df72ef7ca891565
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
