#!/usr/bin/env bash
set -euo pipefail
base_commit=d02e6243cb27c8aded576338f2a33fa4b9d4fa5b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
