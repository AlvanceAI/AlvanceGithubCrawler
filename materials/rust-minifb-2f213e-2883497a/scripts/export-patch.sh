#!/usr/bin/env bash
set -euo pipefail
base_commit=2883497abb4576e93b7d39e823c67137c2157cdf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
