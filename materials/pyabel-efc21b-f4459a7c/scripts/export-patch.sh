#!/usr/bin/env bash
set -euo pipefail
base_commit=f4459a7ce5f62088781b863d0cd08bbb54ed123b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
