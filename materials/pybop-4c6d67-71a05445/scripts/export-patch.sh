#!/usr/bin/env bash
set -euo pipefail
base_commit=71a05445b6d26dd958400e5e3fdef93437331ae3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
