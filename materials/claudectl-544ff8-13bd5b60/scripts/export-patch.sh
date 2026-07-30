#!/usr/bin/env bash
set -euo pipefail
base_commit=13bd5b6036baf35817f155dc24c0d21676b1111e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
