#!/usr/bin/env bash
set -euo pipefail
base_commit=da3cb2092178357bb089de842a20ec2a8053b889
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
