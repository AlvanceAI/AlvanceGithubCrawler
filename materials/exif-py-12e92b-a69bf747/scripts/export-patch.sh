#!/usr/bin/env bash
set -euo pipefail
base_commit=a69bf74770caf6b333221658f5092ed69f99faac
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
