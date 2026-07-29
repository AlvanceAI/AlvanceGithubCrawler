#!/usr/bin/env bash
set -euo pipefail
base_commit=7815e7a913864746073236537e8f5fc133a87ab9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
