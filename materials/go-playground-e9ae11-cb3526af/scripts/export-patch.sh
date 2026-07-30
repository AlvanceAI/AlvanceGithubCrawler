#!/usr/bin/env bash
set -euo pipefail
base_commit=cb3526af1fc084d4a0214878bc4454087e073ca7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
