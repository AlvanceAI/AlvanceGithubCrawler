#!/usr/bin/env bash
set -euo pipefail
base_commit=3cc331ca1cbcda28996a1effc97ecf0760072fe9
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
