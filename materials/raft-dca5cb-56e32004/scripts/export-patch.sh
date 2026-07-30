#!/usr/bin/env bash
set -euo pipefail
base_commit=56e32004b1af3a4cb625fbfe5dbca24fb6023d09
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
