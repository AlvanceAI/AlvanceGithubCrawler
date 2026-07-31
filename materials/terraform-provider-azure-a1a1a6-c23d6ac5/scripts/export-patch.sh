#!/usr/bin/env bash
set -euo pipefail
base_commit=c23d6ac52c89bb76e43285124b5afc419ccbc549
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
