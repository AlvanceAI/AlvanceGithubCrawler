#!/usr/bin/env bash
set -euo pipefail
base_commit=33fe4e06a8da3b5f4a784a0c7ce01a88b295f7ce
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
