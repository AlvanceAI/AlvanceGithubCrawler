#!/usr/bin/env bash
set -euo pipefail
base_commit=7ef2113c52f1b4765287f90ac0741b2051d66fcb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
