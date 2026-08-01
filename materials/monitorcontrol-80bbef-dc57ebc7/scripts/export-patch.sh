#!/usr/bin/env bash
set -euo pipefail
base_commit=dc57ebc7a6003389e2161766ee67b07195e0a713
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
