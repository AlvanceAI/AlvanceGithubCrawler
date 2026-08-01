#!/usr/bin/env bash
set -euo pipefail
base_commit=77ad53e511a93fee7eb0062da575082580a2ea01
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
