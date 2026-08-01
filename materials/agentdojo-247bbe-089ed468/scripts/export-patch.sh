#!/usr/bin/env bash
set -euo pipefail
base_commit=089ed468cf3ed0322acc66b0211f26d9d90dbf60
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
