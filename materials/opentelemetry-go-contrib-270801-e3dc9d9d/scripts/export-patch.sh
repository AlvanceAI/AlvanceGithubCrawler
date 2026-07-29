#!/usr/bin/env bash
set -euo pipefail
base_commit=e3dc9d9daf2179c0ce57b86984e4b927022a3279
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
