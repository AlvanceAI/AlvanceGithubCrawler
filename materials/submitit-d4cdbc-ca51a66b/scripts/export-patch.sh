#!/usr/bin/env bash
set -euo pipefail
base_commit=ca51a66b6da2400468f338133eabdfb4c9a2936c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
