#!/usr/bin/env bash
set -euo pipefail
base_commit=a4c10e977b574114613431394b30412b50aaacce
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
