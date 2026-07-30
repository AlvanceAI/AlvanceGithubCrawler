#!/usr/bin/env bash
set -euo pipefail
base_commit=449e375aa13fcaa02d16f743f93374e27a2c60aa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
