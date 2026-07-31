#!/usr/bin/env bash
set -euo pipefail
base_commit=6fafc2c60b5cbe91378934a9b1b670fb8fc88102
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
