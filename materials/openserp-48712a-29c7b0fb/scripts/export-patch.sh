#!/usr/bin/env bash
set -euo pipefail
base_commit=29c7b0fbe09640160efcfc1f1e04e60e0fbe60e9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
