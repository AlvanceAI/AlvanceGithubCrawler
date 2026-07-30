#!/usr/bin/env bash
set -euo pipefail
base_commit=22de0f36e4f98866d6d154ad2dde74461365220b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
