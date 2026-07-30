#!/usr/bin/env bash
set -euo pipefail
base_commit=f51aaee82475d83426cde0a3def5186fbd43b9a9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
