#!/usr/bin/env bash
set -euo pipefail
base_commit=ade04d0103ff250f7746106eff19d745ebf748d0
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
