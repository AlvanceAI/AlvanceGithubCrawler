#!/usr/bin/env bash
set -euo pipefail
base_commit=a737ac442a9d032f9f824050b23dc9b6d766657e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
