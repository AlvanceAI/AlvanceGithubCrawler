#!/usr/bin/env bash
set -euo pipefail
base_commit=c1e7daacc51acafd62760074b35e215be5e43df3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
