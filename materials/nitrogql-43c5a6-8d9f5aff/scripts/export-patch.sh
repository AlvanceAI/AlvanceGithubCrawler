#!/usr/bin/env bash
set -euo pipefail
base_commit=8d9f5aff1fd6fd18f7190180071772f6aa485c7e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
