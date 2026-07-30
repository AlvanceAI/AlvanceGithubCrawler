#!/usr/bin/env bash
set -euo pipefail
base_commit=0e211203698165419e87355bbe74e32337e5ca2b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
