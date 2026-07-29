#!/usr/bin/env bash
set -euo pipefail
base_commit=122e0ce18a46bfd1576e57763679d23e62418391
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
