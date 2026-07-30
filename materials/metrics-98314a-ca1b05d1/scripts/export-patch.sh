#!/usr/bin/env bash
set -euo pipefail
base_commit=ca1b05d11f437d1f3326ee21805595236d4e5c18
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
