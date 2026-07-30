#!/usr/bin/env bash
set -euo pipefail
base_commit=4c39a8e181182c80b4811e49fb5194626bfcda45
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
