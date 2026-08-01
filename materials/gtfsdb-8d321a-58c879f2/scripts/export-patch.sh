#!/usr/bin/env bash
set -euo pipefail
base_commit=58c879f2c77a930bc8c7fc783d9d5a58585d2ed1
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
