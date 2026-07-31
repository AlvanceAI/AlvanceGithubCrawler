#!/usr/bin/env bash
set -euo pipefail
base_commit=444ae5ed29cfbc767b6592a3f27d5d05ca24b609
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
