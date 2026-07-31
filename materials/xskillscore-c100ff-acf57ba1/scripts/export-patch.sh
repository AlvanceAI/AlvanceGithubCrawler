#!/usr/bin/env bash
set -euo pipefail
base_commit=acf57ba149035bb05d29e19e14940240b4188397
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
