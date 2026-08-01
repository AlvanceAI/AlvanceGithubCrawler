#!/usr/bin/env bash
set -euo pipefail
base_commit=e0eb3ded6ef77269e4a04af4e04e71e4fcfd9f38
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
