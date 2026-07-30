#!/usr/bin/env bash
set -euo pipefail
base_commit=10fe18aaaeed1ab567e794e7ad9ddeaff729b91f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
