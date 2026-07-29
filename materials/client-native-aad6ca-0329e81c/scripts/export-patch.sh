#!/usr/bin/env bash
set -euo pipefail
base_commit=0329e81cc3c6367544f9adbbb57b9374936aafae
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
