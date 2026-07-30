#!/usr/bin/env bash
set -euo pipefail
base_commit=21bb5d175372aa474b44178b8a0577be1822279e
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
