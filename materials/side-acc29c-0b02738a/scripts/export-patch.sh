#!/usr/bin/env bash
set -euo pipefail
base_commit=0b02738aba00d891f270d7f9959bdc0af67e7e08
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
