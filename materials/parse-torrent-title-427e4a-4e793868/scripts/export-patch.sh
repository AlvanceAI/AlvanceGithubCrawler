#!/usr/bin/env bash
set -euo pipefail
base_commit=4e793868512074e49c78e5b714d072f748ab9dc1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
