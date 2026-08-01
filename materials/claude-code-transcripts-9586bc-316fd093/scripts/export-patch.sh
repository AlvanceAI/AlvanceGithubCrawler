#!/usr/bin/env bash
set -euo pipefail
base_commit=316fd093aca3c9c0ad8aa70092711aee3adacc6e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
