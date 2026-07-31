#!/usr/bin/env bash
set -euo pipefail
base_commit=6189c54213a38255c57b8eb0c8015920d79bd70e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
