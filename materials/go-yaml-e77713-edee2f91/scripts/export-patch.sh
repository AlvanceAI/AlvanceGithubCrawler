#!/usr/bin/env bash
set -euo pipefail
base_commit=edee2f91616c6d73112a13e7c0dbde72ce938877
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
