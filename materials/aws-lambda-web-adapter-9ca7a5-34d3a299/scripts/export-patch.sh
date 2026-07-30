#!/usr/bin/env bash
set -euo pipefail
base_commit=34d3a29939ea0c387c145f67cbd7ad72ae833c71
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
