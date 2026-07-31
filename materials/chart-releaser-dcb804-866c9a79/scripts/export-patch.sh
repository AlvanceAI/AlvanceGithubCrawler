#!/usr/bin/env bash
set -euo pipefail
base_commit=866c9a7927ab45ab6560b91393fea97e070778c1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
