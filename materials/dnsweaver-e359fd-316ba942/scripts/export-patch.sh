#!/usr/bin/env bash
set -euo pipefail
base_commit=316ba942857319dd2e394fa422a4d16221df07ef
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
