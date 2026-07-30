#!/usr/bin/env bash
set -euo pipefail
base_commit=39a175e9fd9749832805c0f2750ffe2fb2bdbc00
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
