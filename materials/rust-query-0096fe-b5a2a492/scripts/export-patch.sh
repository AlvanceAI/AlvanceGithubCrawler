#!/usr/bin/env bash
set -euo pipefail
base_commit=b5a2a492c777e378c61072b86cca9e5b01709517
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
