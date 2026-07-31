#!/usr/bin/env bash
set -euo pipefail
base_commit=2167ed1cbe765af7a76e3e863c1308f1f489ecfa
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
