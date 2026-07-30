#!/usr/bin/env bash
set -euo pipefail
base_commit=f2f9e92c405bf71d69433bdbdb84c2ca144bbe92
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
