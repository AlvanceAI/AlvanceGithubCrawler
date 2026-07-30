#!/usr/bin/env bash
set -euo pipefail
base_commit=8c8805c644100735bf9c430bc11d0a5443f5b113
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
