#!/usr/bin/env bash
set -euo pipefail
base_commit=803c4797f017da7192df720475e88b1fd1481b6e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
