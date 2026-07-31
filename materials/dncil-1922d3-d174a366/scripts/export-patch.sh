#!/usr/bin/env bash
set -euo pipefail
base_commit=d174a3664767db00d8ee2a0652af9e7275119334
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
