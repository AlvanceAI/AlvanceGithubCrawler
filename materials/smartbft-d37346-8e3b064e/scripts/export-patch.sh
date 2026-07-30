#!/usr/bin/env bash
set -euo pipefail
base_commit=8e3b064edbfaebd2229b6c21e5c290f7bb91d0f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
