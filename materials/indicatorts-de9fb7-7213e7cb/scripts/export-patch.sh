#!/usr/bin/env bash
set -euo pipefail
base_commit=7213e7cbec2bb96ee37da1318ce9e329d7efeef5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
