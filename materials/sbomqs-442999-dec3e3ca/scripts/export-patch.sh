#!/usr/bin/env bash
set -euo pipefail
base_commit=dec3e3ca06f87f1629140af68024dfcb0a76316d
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
