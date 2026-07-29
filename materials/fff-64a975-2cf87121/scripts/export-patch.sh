#!/usr/bin/env bash
set -euo pipefail
base_commit=2cf871210b7c10cb1bb3e99d54b36125c6b63ed2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
