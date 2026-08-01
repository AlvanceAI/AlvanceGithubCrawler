#!/usr/bin/env bash
set -euo pipefail
base_commit=ec47a7a5095bb5deffc24e9b6812e39107508dbe
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
