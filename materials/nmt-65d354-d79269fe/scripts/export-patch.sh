#!/usr/bin/env bash
set -euo pipefail
base_commit=d79269fe292a382a860d83ca2014f92f72ac93de
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
