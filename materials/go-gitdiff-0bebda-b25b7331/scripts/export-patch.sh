#!/usr/bin/env bash
set -euo pipefail
base_commit=b25b7331c153cdcfabd5c3940c43bc9d9235749c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
