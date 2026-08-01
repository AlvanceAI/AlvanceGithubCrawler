#!/usr/bin/env bash
set -euo pipefail
base_commit=f2bda538aedb4f467cb0615c97e3931ec792e353
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
