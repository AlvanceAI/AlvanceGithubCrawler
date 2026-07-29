#!/usr/bin/env bash
set -euo pipefail
base_commit=554059400962398e03b166ba26f364fa58a25bac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
