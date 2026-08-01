#!/usr/bin/env bash
set -euo pipefail
base_commit=a73776b73dac491f38eed48ced25974f57bc0195
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
