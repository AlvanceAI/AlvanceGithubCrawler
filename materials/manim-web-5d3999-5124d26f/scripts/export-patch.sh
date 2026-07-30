#!/usr/bin/env bash
set -euo pipefail
base_commit=5124d26f9d70d38fd9b1c51f46ec385b5c05afc5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
