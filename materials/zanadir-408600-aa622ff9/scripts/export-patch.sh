#!/usr/bin/env bash
set -euo pipefail
base_commit=aa622ff92ae693b2f570ab13266d39cf672617a4
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
