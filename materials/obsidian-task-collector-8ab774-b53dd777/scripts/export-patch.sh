#!/usr/bin/env bash
set -euo pipefail
base_commit=b53dd7771d21f33d9afee308805af6ac115520e8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
