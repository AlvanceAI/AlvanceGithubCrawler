#!/usr/bin/env bash
set -euo pipefail
base_commit=c7544f6e88fa6f8ea00f7977ecdf6391ac1f81eb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
