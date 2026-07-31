#!/usr/bin/env bash
set -euo pipefail
base_commit=9af4acf0efe1991cbed2952685f05cecb5211d7f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
