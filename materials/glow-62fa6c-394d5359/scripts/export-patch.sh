#!/usr/bin/env bash
set -euo pipefail
base_commit=394d535962b324f7dd84b9244afbd952a4fe717e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
