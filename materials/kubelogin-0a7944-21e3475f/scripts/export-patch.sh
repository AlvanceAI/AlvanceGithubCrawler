#!/usr/bin/env bash
set -euo pipefail
base_commit=21e3475f3922cfcbdbcef7c3b464a2fb38cbea73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
