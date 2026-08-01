#!/usr/bin/env bash
set -euo pipefail
base_commit=8a1eed57f3ab2dff9371e8ce60fb39ac85871e8d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
