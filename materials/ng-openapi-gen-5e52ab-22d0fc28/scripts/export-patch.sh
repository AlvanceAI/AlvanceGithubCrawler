#!/usr/bin/env bash
set -euo pipefail
base_commit=22d0fc28621cd5d264baec26827293d5195fdb1c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
