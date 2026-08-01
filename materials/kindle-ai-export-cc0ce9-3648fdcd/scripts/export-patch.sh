#!/usr/bin/env bash
set -euo pipefail
base_commit=3648fdcd6af71b81ff0578c6bd93e0a2678c7090
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
