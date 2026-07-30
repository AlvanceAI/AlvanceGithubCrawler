#!/usr/bin/env bash
set -euo pipefail
base_commit=886ff6b80d5b9e644783519e2f72278aadb80491
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
