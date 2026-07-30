#!/usr/bin/env bash
set -euo pipefail
base_commit=3c594b1345afd27d8862cb49ea84c7a8a011b2f6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
