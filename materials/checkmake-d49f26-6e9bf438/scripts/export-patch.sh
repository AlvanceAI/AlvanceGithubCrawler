#!/usr/bin/env bash
set -euo pipefail
base_commit=6e9bf438baca255af7c5f608358d2bf9a15af408
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
