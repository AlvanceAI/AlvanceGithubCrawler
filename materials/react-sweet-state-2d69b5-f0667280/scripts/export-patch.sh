#!/usr/bin/env bash
set -euo pipefail
base_commit=f0667280ccfff5033b078db32f65c206b3fae918
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
