#!/usr/bin/env bash
set -euo pipefail
base_commit=69721c61c64115795ea862ff917e8e990f966808
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
