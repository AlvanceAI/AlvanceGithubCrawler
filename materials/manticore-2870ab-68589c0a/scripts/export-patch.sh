#!/usr/bin/env bash
set -euo pipefail
base_commit=68589c0a5aef71131bc9c11ae7c24d6665470810
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
