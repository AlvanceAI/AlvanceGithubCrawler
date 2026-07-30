#!/usr/bin/env bash
set -euo pipefail
base_commit=7e52dc9d27eb32e0dc9f22a924adef28e92da69f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
