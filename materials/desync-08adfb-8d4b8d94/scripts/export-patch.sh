#!/usr/bin/env bash
set -euo pipefail
base_commit=8d4b8d94e99edd424ea07219cbc5b55446ee7c10
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
