#!/usr/bin/env bash
set -euo pipefail
base_commit=65482925407ce3eec04f040b8bd4ecdb608e709c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
