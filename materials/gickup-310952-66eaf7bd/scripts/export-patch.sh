#!/usr/bin/env bash
set -euo pipefail
base_commit=66eaf7bd2cc80fb9cb13f113c3a17d7c25e42baf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
