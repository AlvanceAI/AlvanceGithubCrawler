#!/usr/bin/env bash
set -euo pipefail
base_commit=a93166653dd978aaaa64f9f84bf37a4e94e0c7cd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
