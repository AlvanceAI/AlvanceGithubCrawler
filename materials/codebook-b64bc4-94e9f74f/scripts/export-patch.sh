#!/usr/bin/env bash
set -euo pipefail
base_commit=94e9f74f9e23db31e7665c5854a06ea4171a7dc2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
