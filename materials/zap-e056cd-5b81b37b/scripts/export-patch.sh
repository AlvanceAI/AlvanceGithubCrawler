#!/usr/bin/env bash
set -euo pipefail
base_commit=5b81b37b81b8e2ed447a6f57991e372ee4fa5c8f
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
