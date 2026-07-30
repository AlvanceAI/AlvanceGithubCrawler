#!/usr/bin/env bash
set -euo pipefail
base_commit=828f4277d1d83dafe6e1849ff10c955d59fa7c6d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
