#!/usr/bin/env bash
set -euo pipefail
base_commit=c0afe3bf819756eab3dd9a32553ec49fae513105
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
