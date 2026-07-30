#!/usr/bin/env bash
set -euo pipefail
base_commit=becdae87cb6a982927ef54938c3e9fdea3edf699
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
