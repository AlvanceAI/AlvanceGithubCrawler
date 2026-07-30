#!/usr/bin/env bash
set -euo pipefail
base_commit=80d7d36aab816e4859aad049af563aff48fa6b62
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
