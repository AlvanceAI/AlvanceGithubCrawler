#!/usr/bin/env bash
set -euo pipefail
base_commit=83a3a9d0a241fb193140807e4e77e81545f6f60d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
