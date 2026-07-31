#!/usr/bin/env bash
set -euo pipefail
base_commit=186b71a415649a85d557ea519cc3305dc7668a04
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
