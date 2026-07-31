#!/usr/bin/env bash
set -euo pipefail
base_commit=d454ba081585288f7416e57dc21b34e7264a94e0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
