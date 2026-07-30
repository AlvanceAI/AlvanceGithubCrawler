#!/usr/bin/env bash
set -euo pipefail
base_commit=aafad4c992694561dba87e0cd21fea9fbdea437d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
