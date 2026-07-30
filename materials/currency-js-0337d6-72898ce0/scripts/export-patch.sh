#!/usr/bin/env bash
set -euo pipefail
base_commit=72898ce024509ddfbe75d14a07e1a5f4c1bdd03a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
