#!/usr/bin/env bash
set -euo pipefail
base_commit=1bc406e1f441577c4e421fc51aba2ab67fbd97fb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
