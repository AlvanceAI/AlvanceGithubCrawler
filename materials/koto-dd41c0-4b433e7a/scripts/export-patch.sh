#!/usr/bin/env bash
set -euo pipefail
base_commit=4b433e7a7ce17957aa4564c80fcaaa46b88fadd2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
