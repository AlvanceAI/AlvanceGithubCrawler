#!/usr/bin/env bash
set -euo pipefail
base_commit=46bbc33bcc3e87446d2590b0d4dd1719ce77566b
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
