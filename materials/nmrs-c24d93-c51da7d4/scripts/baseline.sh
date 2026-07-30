#!/usr/bin/env bash
set -euo pipefail
cd /app
exec env CARGO_HOME=/usr/local/cargo HOME=/root PATH=/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin RUSTUP_HOME=/usr/local/rustup sh -c 'cargo test'
