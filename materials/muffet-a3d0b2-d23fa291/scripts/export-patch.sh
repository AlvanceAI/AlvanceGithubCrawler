#!/usr/bin/env bash
set -euo pipefail
base_commit=d23fa291377674f8df5bbfecd840cee2c3029633
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
