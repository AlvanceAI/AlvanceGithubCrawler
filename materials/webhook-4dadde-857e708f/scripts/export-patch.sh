#!/usr/bin/env bash
set -euo pipefail
base_commit=857e708f87a610ecddb44397d90e5b3e97e4315a
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
