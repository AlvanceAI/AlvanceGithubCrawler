#!/usr/bin/env bash
set -euo pipefail
base_commit=a399063e89181faddd69fd4e6c001a9ac25c7462
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
