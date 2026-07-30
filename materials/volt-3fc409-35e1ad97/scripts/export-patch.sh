#!/usr/bin/env bash
set -euo pipefail
base_commit=35e1ad972298896f2d480183e08d4a6142b8ed84
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
