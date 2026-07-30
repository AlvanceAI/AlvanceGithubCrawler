#!/usr/bin/env bash
set -euo pipefail
base_commit=b4aaee797cc3fd12e8194db406d9d73a6bc021ce
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
