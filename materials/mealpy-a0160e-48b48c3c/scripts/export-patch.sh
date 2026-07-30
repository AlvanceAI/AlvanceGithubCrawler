#!/usr/bin/env bash
set -euo pipefail
base_commit=48b48c3c6696fca077b5aaf278ba6ccdefb021b9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
