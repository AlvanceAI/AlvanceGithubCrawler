#!/usr/bin/env bash
set -euo pipefail
base_commit=db0aac244a22cdef5f46bae37c07b4b3c96aeb58
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
