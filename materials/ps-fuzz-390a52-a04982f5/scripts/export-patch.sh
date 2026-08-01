#!/usr/bin/env bash
set -euo pipefail
base_commit=a04982f58fe6c99b08df12a69e967368c96ef9f4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
