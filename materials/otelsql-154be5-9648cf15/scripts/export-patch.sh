#!/usr/bin/env bash
set -euo pipefail
base_commit=9648cf15c51dc4cecafb23587acd7d76ec1ffbac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
