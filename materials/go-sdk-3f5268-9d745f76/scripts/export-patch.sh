#!/usr/bin/env bash
set -euo pipefail
base_commit=9d745f76a46e23ae0d022f1abb098132b67603e5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
