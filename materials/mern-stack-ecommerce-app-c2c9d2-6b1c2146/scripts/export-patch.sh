#!/usr/bin/env bash
set -euo pipefail
base_commit=6b1c21466b192f53724e6ea9d6622b6c0cbb0eed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
