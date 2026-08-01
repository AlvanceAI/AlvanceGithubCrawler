#!/usr/bin/env bash
set -euo pipefail
base_commit=e1bc7c0071f5be150cb7ec2efcefec3efa1f5685
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
