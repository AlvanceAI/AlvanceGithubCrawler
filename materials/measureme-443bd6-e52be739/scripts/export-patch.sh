#!/usr/bin/env bash
set -euo pipefail
base_commit=e52be7399403fab879ed034cf0b6bdba431d39b5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
