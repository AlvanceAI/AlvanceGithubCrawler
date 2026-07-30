#!/usr/bin/env bash
set -euo pipefail
base_commit=830281cdda4b11b181133fe78c9daa72e6021057
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
