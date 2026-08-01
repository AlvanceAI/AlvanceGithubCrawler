#!/usr/bin/env bash
set -euo pipefail
base_commit=6771b6d4600d9929880f77e7fce618887b850f73
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
