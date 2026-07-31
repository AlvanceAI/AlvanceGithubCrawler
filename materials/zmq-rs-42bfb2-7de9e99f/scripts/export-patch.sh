#!/usr/bin/env bash
set -euo pipefail
base_commit=7de9e99f0a810857cfd001134c924c0556a2451a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
