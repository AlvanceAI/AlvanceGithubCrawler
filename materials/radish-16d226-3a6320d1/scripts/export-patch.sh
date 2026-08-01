#!/usr/bin/env bash
set -euo pipefail
base_commit=3a6320d129f123e2decb2a8485264c2f08bf83e7
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
