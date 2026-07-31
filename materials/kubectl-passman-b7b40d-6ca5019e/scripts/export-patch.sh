#!/usr/bin/env bash
set -euo pipefail
base_commit=6ca5019e64432d1afdaf250be3e284f36486daf5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
