#!/usr/bin/env bash
set -euo pipefail
base_commit=1d8a98301cc2c6d37c6beb82589f5e59092a792c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
