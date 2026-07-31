#!/usr/bin/env bash
set -euo pipefail
base_commit=c16f8a9a132cc666c5fe387a3d7946d54f8e15aa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
