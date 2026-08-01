#!/usr/bin/env bash
set -euo pipefail
base_commit=ea9a4803463817393c1da6ce486e42ebd7eac341
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
