#!/usr/bin/env bash
set -euo pipefail
base_commit=3f30d38556e93b89231d7c11ef7ef93faf525d90
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
