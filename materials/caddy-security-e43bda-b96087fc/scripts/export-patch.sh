#!/usr/bin/env bash
set -euo pipefail
base_commit=b96087fc696ada2ed80f4ca81e031878a47d43ac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
