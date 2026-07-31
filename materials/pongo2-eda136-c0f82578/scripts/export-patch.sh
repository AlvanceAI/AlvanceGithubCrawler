#!/usr/bin/env bash
set -euo pipefail
base_commit=c0f82578df571c69ce46d4af5ba2f358d98c98e6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
