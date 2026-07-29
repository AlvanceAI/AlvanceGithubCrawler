#!/usr/bin/env bash
set -euo pipefail
base_commit=947c3caaf08a6958180168f0b9f1289f722a18a8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
