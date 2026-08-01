#!/usr/bin/env bash
set -euo pipefail
base_commit=aea5b4b7e17005755445d8824c0376c90ad80f61
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
