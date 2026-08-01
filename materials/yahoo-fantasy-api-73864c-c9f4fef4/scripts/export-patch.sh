#!/usr/bin/env bash
set -euo pipefail
base_commit=c9f4fef444a521022579ba38e4721f0a780f66c6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
