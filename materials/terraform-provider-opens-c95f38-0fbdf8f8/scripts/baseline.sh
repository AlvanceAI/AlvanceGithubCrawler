#!/usr/bin/env bash
set -euo pipefail
cd /app
exec env GOCACHE=/root/.cache/go-build GOMODCACHE=/go/pkg/mod GOPATH=/go GOPROXY=https://goproxy.cn,direct GOTOOLCHAIN=go1.25.10+auto HOME=/root PATH=/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh -c 'go test ./...'
