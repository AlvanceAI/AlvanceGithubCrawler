#!/usr/bin/env bash
set -euo pipefail
base_commit=5d664cda8d54d52c0810a485dd93bbf747054ba8
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
