#!/usr/bin/env bash
set -euo pipefail
base_commit=c0033996db6b4b0079099655b5b3600da5610724
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
