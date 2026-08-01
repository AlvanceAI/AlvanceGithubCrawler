#!/usr/bin/env bash
set -euo pipefail
base_commit=04426773402214b1ad18f93bca760e1ccf74a688
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
