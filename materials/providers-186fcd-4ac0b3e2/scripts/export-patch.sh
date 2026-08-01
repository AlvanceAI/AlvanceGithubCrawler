#!/usr/bin/env bash
set -euo pipefail
base_commit=4ac0b3e2df7de682a95d50e3429dadb0995862cf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
