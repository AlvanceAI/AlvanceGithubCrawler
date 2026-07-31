#!/usr/bin/env bash
set -euo pipefail
base_commit=9f324d51cdef3b07d2f3678b4fec05343087cf49
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
