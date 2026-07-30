#!/usr/bin/env bash
set -euo pipefail
base_commit=ecfa08c1a13fdb5c8e225c040c5254a891a80acd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
