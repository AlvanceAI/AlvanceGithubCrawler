#!/usr/bin/env bash
set -euo pipefail
base_commit=6475422180edc38f4f214effbbf980f78e7a3e7a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
