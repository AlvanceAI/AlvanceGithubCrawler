#!/usr/bin/env bash
set -euo pipefail
base_commit=e34a0fa0cab49a65c0e27475e9776a8d848bddcc
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
