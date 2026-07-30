#!/usr/bin/env bash
set -euo pipefail
base_commit=3f4c582dd62ec2e1df5b20ff98163e375948ab60
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
