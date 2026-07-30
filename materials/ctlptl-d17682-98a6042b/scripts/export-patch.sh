#!/usr/bin/env bash
set -euo pipefail
base_commit=98a6042bc12ce538fa84d699d7e94aa3efb479f5
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
