#!/usr/bin/env bash
set -euo pipefail
base_commit=fa34b68c0c1d62dcae0c0bfefcc27224f560d599
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
