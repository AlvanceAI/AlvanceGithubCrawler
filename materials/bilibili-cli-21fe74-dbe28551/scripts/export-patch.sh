#!/usr/bin/env bash
set -euo pipefail
base_commit=dbe28551930df43b633baa52e9639832aeada967
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
