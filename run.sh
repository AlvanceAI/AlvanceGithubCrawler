#!/usr/bin/env bash
set -Eeuo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$repo_root"

if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required; install it from https://docs.astral.sh/uv/" >&2
    exit 2
fi

exec uv run python monitor.py "$@"
