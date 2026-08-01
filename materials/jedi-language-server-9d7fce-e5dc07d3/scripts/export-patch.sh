#!/usr/bin/env bash
set -euo pipefail
base_commit=e5dc07d31d09632a5fd74d0109c79298cb6900ec
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
