#!/usr/bin/env bash
set -euo pipefail
base_commit=2df6962734785c5099589c89a0b6241ac5836b47
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
