#!/usr/bin/env bash
set -euo pipefail
base_commit=0d7f34bb3feba6cbd670d244fe707621be7f7c69
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
