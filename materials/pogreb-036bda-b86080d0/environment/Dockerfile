FROM docker.io/library/golang:1.22
USER root
ENV GOCACHE="/root/.cache/go-build"
ENV GOMODCACHE="/go/pkg/mod"
ENV GOPATH="/go"
ENV GOPROXY="https://goproxy.cn,direct"
ENV GOTOOLCHAIN="local"
ENV HOME="/root"
ENV PATH="/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/go/bin/go version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/akrylysov/pogreb.git && git fetch --depth=1 origin b86080d06267f8d12067cd432ffd9e5b6916d354 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = b86080d06267f8d12067cd432ffd9e5b6916d354 && test "$(git rev-parse HEAD^{tree})" = 4fb8b70c2c00089923c10bc394d2694e433ee08e
WORKDIR /app
RUN /usr/local/go/bin/go mod download
RUN /usr/local/go/bin/go build ./...
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
