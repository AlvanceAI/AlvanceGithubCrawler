#!/usr/bin/env bash
set -euo pipefail
base_commit=5a0bac50e0a57c8bbf470f05ddef8319b4ad0314
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
