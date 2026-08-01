#!/usr/bin/env bash
set -euo pipefail
base_commit=c34cb91f980315bdca40b59645c5b48c0c426d64
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
