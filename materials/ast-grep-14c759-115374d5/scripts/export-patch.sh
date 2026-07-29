#!/usr/bin/env bash
set -euo pipefail
base_commit=115374d5db7a086d6da1bb67162a85febe818937
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
