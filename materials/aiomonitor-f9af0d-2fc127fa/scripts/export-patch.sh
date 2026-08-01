#!/usr/bin/env bash
set -euo pipefail
base_commit=2fc127facaf7cd6ffefe6aba5a6856a59b178403
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
