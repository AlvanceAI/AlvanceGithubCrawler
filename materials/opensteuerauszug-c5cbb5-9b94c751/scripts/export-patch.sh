#!/usr/bin/env bash
set -euo pipefail
base_commit=9b94c7514a2621419bc888cd4729d459a910f698
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
