#!/usr/bin/env bash
set -euo pipefail
base_commit=1899870cea8bb377948f05cfea64733ec6ea2cd6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
