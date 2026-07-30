#!/usr/bin/env bash
set -euo pipefail
base_commit=cd58d7ee005b29f679acc9b72c5c4fe09fab316c
cd /app
mkdir -p /logs/artifacts
git diff --binary "$base_commit" HEAD > /logs/artifacts/model.patch
