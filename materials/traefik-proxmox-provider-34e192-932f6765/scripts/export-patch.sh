#!/usr/bin/env bash
set -euo pipefail
base_commit=932f676582707dc3a61cb5c85092a766fef87b53
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
