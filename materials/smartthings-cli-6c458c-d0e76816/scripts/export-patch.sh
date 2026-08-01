#!/usr/bin/env bash
set -euo pipefail
base_commit=d0e76816b56608fb827ee3bac0c09b31d92b9388
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
