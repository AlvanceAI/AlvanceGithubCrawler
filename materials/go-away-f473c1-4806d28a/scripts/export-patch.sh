#!/usr/bin/env bash
set -euo pipefail
base_commit=4806d28a3299ab6e99d14801197027c36db268b2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
