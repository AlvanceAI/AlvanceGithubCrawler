#!/usr/bin/env bash
set -euo pipefail
base_commit=7d03fd265228717069000df70e797df70d47c6a6
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
