#!/usr/bin/env bash
set -euo pipefail
base_commit=559575c619ec5792150d6568e3770d43f728f2a7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
