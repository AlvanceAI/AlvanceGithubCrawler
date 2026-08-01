#!/usr/bin/env bash
set -euo pipefail
base_commit=fb2022664af3e081f4016e6c21b84b136b74082c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
