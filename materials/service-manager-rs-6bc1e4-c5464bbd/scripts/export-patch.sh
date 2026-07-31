#!/usr/bin/env bash
set -euo pipefail
base_commit=c5464bbd5d9f9b586d49581140ada7e3e9f01c61
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
