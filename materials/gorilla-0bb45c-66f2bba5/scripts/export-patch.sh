#!/usr/bin/env bash
set -euo pipefail
base_commit=66f2bba5a20224be81598051e6474bf5c9221164
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
