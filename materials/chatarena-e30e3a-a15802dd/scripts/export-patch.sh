#!/usr/bin/env bash
set -euo pipefail
base_commit=a15802dd89c0d69165bb0b07e70c2bac5a7c4e36
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
