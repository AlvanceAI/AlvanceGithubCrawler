#!/usr/bin/env bash
set -euo pipefail
base_commit=3e046e4dfabd98ef667ed0e5a058fd673c06a479
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
