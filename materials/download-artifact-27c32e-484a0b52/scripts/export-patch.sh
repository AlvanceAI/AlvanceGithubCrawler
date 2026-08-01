#!/usr/bin/env bash
set -euo pipefail
base_commit=484a0b528fb4d7bd804637ccb632e47a0e638317
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
