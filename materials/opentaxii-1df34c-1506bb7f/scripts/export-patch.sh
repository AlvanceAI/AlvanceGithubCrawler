#!/usr/bin/env bash
set -euo pipefail
base_commit=1506bb7f54c2da3e839ccdfd5c5bcd16c928a9ac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
