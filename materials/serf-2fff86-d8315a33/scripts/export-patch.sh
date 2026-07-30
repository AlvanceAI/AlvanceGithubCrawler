#!/usr/bin/env bash
set -euo pipefail
base_commit=d8315a3368de1cf5f798f358cded9c7e771d387c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
