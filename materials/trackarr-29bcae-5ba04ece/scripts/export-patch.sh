#!/usr/bin/env bash
set -euo pipefail
base_commit=5ba04ececa35c80fbebe51a8483ccd6fe916bb62
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
