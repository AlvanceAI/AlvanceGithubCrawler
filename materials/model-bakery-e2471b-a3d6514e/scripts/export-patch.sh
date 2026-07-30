#!/usr/bin/env bash
set -euo pipefail
base_commit=a3d6514e60a39dadc72ebefcf951737854835300
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
