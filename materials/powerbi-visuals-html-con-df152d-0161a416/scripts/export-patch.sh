#!/usr/bin/env bash
set -euo pipefail
base_commit=0161a41638bfa44d641d60742fff6d924cf68828
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
