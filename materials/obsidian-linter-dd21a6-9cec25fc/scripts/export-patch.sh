#!/usr/bin/env bash
set -euo pipefail
base_commit=9cec25fcfd5289076afddc3c58e72b7e57436bf2
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
