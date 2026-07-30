#!/usr/bin/env bash
set -euo pipefail
base_commit=47c09b923d9a646fe6d71515edcc497156f4f356
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
