#!/usr/bin/env bash
set -euo pipefail
base_commit=e0fc705e4a36cc6ed330967dc4967bdc3f092dcd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
