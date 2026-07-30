#!/usr/bin/env bash
set -euo pipefail
base_commit=0683146d967b5677c02fd976ef262fe38603bbfd
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
