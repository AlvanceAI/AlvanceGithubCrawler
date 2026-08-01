#!/usr/bin/env bash
set -euo pipefail
base_commit=34274e3256c286b0d450916a3066fe4b7264cd50
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
