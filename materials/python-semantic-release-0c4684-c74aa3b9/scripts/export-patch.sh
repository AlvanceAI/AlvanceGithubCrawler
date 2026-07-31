#!/usr/bin/env bash
set -euo pipefail
base_commit=c74aa3b99de6d9c721f8bd6d2abfa142298b94c9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
