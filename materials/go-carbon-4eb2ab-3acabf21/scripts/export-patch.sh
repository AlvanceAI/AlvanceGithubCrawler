#!/usr/bin/env bash
set -euo pipefail
base_commit=3acabf21eb31bfadf3fb4bd61f9ce450f223c5ce
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
