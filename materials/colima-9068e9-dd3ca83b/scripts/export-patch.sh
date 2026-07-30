#!/usr/bin/env bash
set -euo pipefail
base_commit=dd3ca83bada3191e1574983660a7a7ce32273cb3
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
