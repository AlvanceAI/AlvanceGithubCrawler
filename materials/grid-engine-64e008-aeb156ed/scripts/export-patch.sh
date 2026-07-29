#!/usr/bin/env bash
set -euo pipefail
base_commit=aeb156ed52a9925354b37933e3901994c8bc7aed
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
