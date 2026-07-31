#!/bin/sh
set -u
mkdir -p /logs/verifier
cd /app
if env CARGO_HOME=/usr/local/cargo HOME=/root PATH=/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin RUSTUP_HOME=/usr/local/rustup sh -c 'cargo test'; then
    echo 1 > /logs/verifier/reward.txt
    exit 0
else
    status=$?
    echo 0 > /logs/verifier/reward.txt
    exit "$status"
fi
