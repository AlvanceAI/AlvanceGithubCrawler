#!/usr/bin/env bash
set -euo pipefail
base_commit=dafe3a581f7f0a1fe15556e30a5becd531756b28
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
