#!/usr/bin/env bash
set -euo pipefail
base_commit=db84eff6c53be7e7619400b7999e0aa550b77536
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
