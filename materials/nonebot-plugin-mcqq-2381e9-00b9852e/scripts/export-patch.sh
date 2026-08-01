#!/usr/bin/env bash
set -euo pipefail
base_commit=00b9852e32387ad742e68984410f2dda308c866c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
