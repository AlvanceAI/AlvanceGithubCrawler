#!/usr/bin/env bash
set -euo pipefail
base_commit=4cef8b4426ec562f61d193adce45fc9689df4d7e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
