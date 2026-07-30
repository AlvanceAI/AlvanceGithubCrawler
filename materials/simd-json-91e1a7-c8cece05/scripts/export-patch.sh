#!/usr/bin/env bash
set -euo pipefail
base_commit=c8cece05a69a379ddc229f63e20701e34c87ef59
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
