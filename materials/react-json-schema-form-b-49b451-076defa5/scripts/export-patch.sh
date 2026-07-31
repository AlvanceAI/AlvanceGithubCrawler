#!/usr/bin/env bash
set -euo pipefail
base_commit=076defa5b409c1acb27a5fc14a1ce493edcf9dcf
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
