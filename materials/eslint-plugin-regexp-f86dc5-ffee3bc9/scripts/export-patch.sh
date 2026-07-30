#!/usr/bin/env bash
set -euo pipefail
base_commit=ffee3bc95e1572ec7f20a46b9db5e19195a3b7bf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
