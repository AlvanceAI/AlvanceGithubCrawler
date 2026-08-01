#!/usr/bin/env bash
set -euo pipefail
base_commit=8092917041f0ae02cbe4c6982deddc931c6adecd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
