#!/usr/bin/env bash
set -euo pipefail
base_commit=d8131fb8f3100dacfc663ec0d1c1c272af219929
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
