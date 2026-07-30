#!/usr/bin/env bash
set -euo pipefail
base_commit=43bb79bd99be984ed510c33e8dcb28b460b7e8cb
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
