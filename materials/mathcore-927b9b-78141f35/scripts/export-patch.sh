#!/usr/bin/env bash
set -euo pipefail
base_commit=78141f35f20a572783fbe60cb4baf5bd0b165358
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
