#!/usr/bin/env bash
set -euo pipefail
base_commit=4c7e0e1174ac1ead032efe28d86428bbbe0ae145
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
