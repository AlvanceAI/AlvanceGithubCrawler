#!/usr/bin/env bash
set -euo pipefail
base_commit=456ede4b723fee185bd0022193e3cfa856e967c3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
